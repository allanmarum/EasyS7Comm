"""High-level client wrapper for EasyS7Comm."""

from __future__ import annotations

from typing import Any

import snap7

from .exceptions import S7AddressError, S7CommunicationError
from .plc_parse_address import PlcParseAddress
from .plc_reader import PLCReader
from .plc_types import DataType
from .plc_writer import PLCWriter


class S7Client:
    """Simplified client for reading and writing Siemens PLC data.

    The class wraps :mod:`snap7` with sensible defaults and convenience methods
    such as :meth:`read_int` and :meth:`write_int`. It expects Siemens-style
    addresses (e.g., ``"DB1.DBW0"`` or ``"Q0.0"``) and automatically handles
    the appropriate Snap7 area operations.

    Example:
        ```python
        from easys7comm import S7Client

        client = S7Client("192.168.0.10")
        client.connect()
        speed = client.read_real("DB1.DBD0")
        client.write_bool("Q0.0", True)
        client.disconnect()
        ```
    """

    def __init__(
        self,
        ip: str,
        rack: int = 0,
        slot: int = 1,
        *,
        port: int = 102,
        auto_connect: bool = False,
    ) -> None:
        """Create a new client instance.

        Args:
            ip: IP address of the target PLC.
            rack: Rack number (default ``0``).
            slot: Slot number (default ``1``).
            port: Communication port, typically ``102``.
            auto_connect: When ``True``, the client connects immediately.

        Raises:
            S7CommunicationError: If automatic connection fails.
        """

        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.port = port
        self.client = snap7.client.Client()

        if auto_connect:
            self.connect()

    def connect(self) -> None:
        """Open a connection to the PLC.

        Raises:
            S7CommunicationError: If a network or Snap7 error occurs.
        """

        try:
            self.client.connect(self.ip, self.rack, self.slot, self.port)
        except Exception as exc:  # pragma: no cover - depends on snap7
            raise S7CommunicationError(f"Failed to connect to PLC at {self.ip}:{self.port}: {exc}") from exc

        if not self.client.get_connected():
            raise S7CommunicationError(f"Connection to PLC at {self.ip}:{self.port} could not be established.")

    def disconnect(self) -> None:
        """Close the PLC connection if active."""

        if self.client.get_connected():
            self.client.disconnect()
        self.client.destroy()

    def _read(self, address: str, data_type: DataType) -> Any:
        """Internal helper that delegates to :class:`PLCReader`.

        Args:
            address: PLC memory address using Siemens notation.
            data_type: Expected :class:`DataType` of the value.

        Returns:
            The parsed Python value.

        Raises:
            S7AddressError: If the address string is invalid.
            S7CommunicationError: If the Snap7 read operation fails.
        """

        try:
            PlcParseAddress.parse_address(address)
        except ValueError as exc:
            raise S7AddressError(str(exc)) from exc

        try:
            return PLCReader(self.client).read(address, data_type)
        except Exception as exc:  # pragma: no cover - depends on snap7
            raise S7CommunicationError(f"Failed to read '{address}': {exc}") from exc

    def _write(self, address: str, value: Any, data_type: DataType) -> None:
        """Internal helper that delegates to :class:`PLCWriter`.

        Args:
            address: PLC memory address using Siemens notation.
            value: Value to persist in the PLC.
            data_type: :class:`DataType` that describes how to write the value.

        Raises:
            S7AddressError: If the address string is invalid.
            S7CommunicationError: If the Snap7 write operation fails.
        """

        try:
            PlcParseAddress.parse_address(address)
        except ValueError as exc:
            raise S7AddressError(str(exc)) from exc

        try:
            PLCWriter(self.client).write(address, value, data_type)
        except Exception as exc:  # pragma: no cover - depends on snap7
            raise S7CommunicationError(f"Failed to write '{address}': {exc}") from exc

    def read_int(self, address: str) -> int:
        """Read a 16-bit signed integer from the PLC.

        Args:
            address: Siemens-formatted address, such as ``"DB1.DBW0"``.

        Returns:
            The integer value read from the PLC.
        """

        return int(self._read(address, DataType.INT))

    def write_int(self, address: str, value: int) -> None:
        """Write a 16-bit signed integer to the PLC.

        Args:
            address: Siemens-formatted address, such as ``"DB1.DBW0"``.
            value: Integer value to write.
        """

        self._write(address, value, DataType.INT)

    def read_real(self, address: str) -> float:
        """Read a 32-bit floating-point value from the PLC.

        Args:
            address: Siemens-formatted address, such as ``"DB1.DBD0"``.

        Returns:
            Floating-point value read from the PLC.
        """

        return float(self._read(address, DataType.REAL))

    def write_real(self, address: str, value: float) -> None:
        """Write a 32-bit floating-point value to the PLC.

        Args:
            address: Siemens-formatted address, such as ``"DB1.DBD0"``.
            value: Floating-point value to write.
        """

        self._write(address, value, DataType.REAL)

    def read_bool(self, address: str) -> bool:
        """Read a boolean flag from the PLC memory."""

        return bool(self._read(address, DataType.BOOL))

    def write_bool(self, address: str, value: bool) -> None:
        """Write a boolean flag to the PLC memory."""

        self._write(address, value, DataType.BOOL)

    def read_dint(self, address: str) -> int:
        """Read a 32-bit signed integer from the PLC."""

        return int(self._read(address, DataType.DINT))

    def write_dint(self, address: str, value: int) -> None:
        """Write a 32-bit signed integer to the PLC."""

        self._write(address, value, DataType.DINT)

    def read_bytes(self, address: str, length: int) -> bytes:
        """Read a raw byte sequence from a DB area.

        Args:
            address: Base address for the byte array (e.g., ``"DB1.DBB0"``).
            length: Number of bytes to read.

        Returns:
            A ``bytes`` object with the requested data.
        """

        parsed = PlcParseAddress.parse_address(address)
        if parsed["address_category"] != "DB":
            raise S7AddressError("Raw byte reads are only supported for DB addresses.")

        try:
            data = self.client.db_read(parsed["db"], parsed["byte_offset"], length)
        except Exception as exc:  # pragma: no cover - depends on snap7
            raise S7CommunicationError(f"Failed to read bytes from '{address}': {exc}") from exc

        return bytes(data)

    def write_bytes(self, address: str, data: bytes) -> None:
        """Write a raw byte sequence into a DB area.

        Args:
            address: Base address for the byte array (e.g., ``"DB1.DBB0"``).
            data: Byte sequence to persist.
        """

        parsed = PlcParseAddress.parse_address(address)
        if parsed["address_category"] != "DB":
            raise S7AddressError("Raw byte writes are only supported for DB addresses.")

        try:
            self.client.db_write(parsed["db"], parsed["byte_offset"], bytearray(data))
        except Exception as exc:  # pragma: no cover - depends on snap7
            raise S7CommunicationError(f"Failed to write bytes to '{address}': {exc}") from exc
