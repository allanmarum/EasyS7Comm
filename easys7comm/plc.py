# easys7comm/plc.py

"""
PLC Abstraction Module

This module provides a high-level abstraction for interacting with a PLC 
using the snap7 library. It simplifies reading and writing data by 
encapsulating connection management and operations.

Usage example:
    plc = PLC("192.168.0.1")
    if plc.get_connected():
        value = plc.read("DB1.DBD0", DataType.REAL)
        plc.write("DB1.DBD0", 42.5, DataType.REAL)
    plc.close()
"""

import snap7
from .plc_reader import PLCReader
from .plc_writer import PLCWriter
from .plc_types import DataType


class PLC:
    """A high-level interface for communicating with a Siemens PLC."""

    def __init__(self, ip: str, rack: int = 0, slot: int = 1, *, auto_connect: bool = True):
        """Create a PLC object with connection parameters.

        Args:
            ip: Target PLC IP address.
            rack: Rack number. Defaults to ``0``.
            slot: Slot number. Defaults to ``1``.
            auto_connect: When ``True`` a connection attempt is made immediately.

        Raises:
            ConnectionError: If automatic connection cannot be established.
        """

        self.ip = ip
        self.rack = rack
        self.slot = slot

        self.client = snap7.client.Client()

        if auto_connect:
            self.connect()

    def connect(self) -> None:
        """Establish a connection with the PLC."""

        try:
            self.client.connect(self.ip, self.rack, self.slot)
        except Exception as exc:
            raise ConnectionError(f"Failed to connect to PLC at {self.ip}: {exc}") from exc

    def get_connected(self) -> bool:
        """Check if the PLC is currently connected."""

        return self.client.get_connected()

    def read(self, address: str, data_type: DataType):
        """Read a value from the PLC at the specified memory address.

        Args:
            address: Memory address to read (e.g., ``"DB1.DBD0"``).
            data_type: :class:`DataType` used to parse the response.

        Returns:
            Value read from the PLC.
        """

        reader = PLCReader(self.client)
        return reader.read(address, data_type)

    def write(self, address: str, value, data_type: DataType):
        """Write a value to the PLC at the specified memory address.

        Args:
            address: Memory address to write to (e.g., ``"DB1.DBD0"``).
            value: Value to write.
            data_type: :class:`DataType` describing ``value``.
        """

        writer = PLCWriter(self.client)
        return writer.write(address, value, data_type)

    def close(self) -> None:
        """Close the connection to the PLC."""

        if self.client.get_connected():
            self.client.disconnect()
        self.client.destroy()
