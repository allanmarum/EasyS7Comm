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
    """
    A high-level interface for communicating with a Siemens PLC.

    This class provides methods for connecting to the PLC, reading data, 
    writing data, and managing the connection lifecycle.
    """

    def __init__(self, ip: str, rack: int = 0, slot: int = 1, *, auto_connect: bool = True):
        """
        Initializes a PLC object with the given IP address, rack and slot.

        Parameters
        ----------
        ip:
            The PLC's IP address.
        rack:
            The rack number. Defaults to ``0``.
        slot:
            The slot number. Defaults to ``1``.
        auto_connect:
            When ``True`` (default) a connection to the PLC is attempted
            immediately.  Set to ``False`` to postpone the connection until
            :meth:`connect` is called.  This is useful for testing or when the
            network might be unavailable during object construction.

        Raises
        ------
        ConnectionError
            If ``auto_connect`` is ``True`` and the connection cannot be
            established.
        """
        self.ip = ip
        self.rack = rack
        self.slot = slot

        # Client instance used for all communications
        self.client = snap7.client.Client()

        if auto_connect:
            self.connect()

    def connect(self) -> None:
        """Establishes a connection with the PLC.

        This method can be called manually when ``auto_connect`` is disabled in
        the constructor.  It will raise a :class:`ConnectionError` if the
        underlying snap7 client fails to connect.
        """
        try:
            self.client.connect(self.ip, self.rack, self.slot)
        except Exception as exc:
            raise ConnectionError(
                f"Failed to connect to PLC at {self.ip}: {exc}"
            ) from exc

    def get_connected(self) -> bool:
        """
        Checks if the PLC is currently connected.

        Returns:
            bool: True if the PLC is connected, False otherwise.
        """
        return self.client.get_connected()

    def read(self, address: str, data_type: DataType):
        """
        Reads a value from the PLC at the specified memory address.

        Args:
            address (str): The memory address to read (e.g., "DB1.DBD0").
            data_type (DataType): The data type to interpret the value.

        Returns:
            Any: The value read from the PLC.
        """
        reader = PLCReader(self.client)
        return reader.read(address, data_type)

    def write(self, address: str, value, data_type: DataType):
        """
        Writes a value to the PLC at the specified memory address.

        Args:
            address (str): The memory address to write to (e.g., "DB1.DBD0").
            value (Any): The value to write.
            data_type (DataType): The data type of the value.

        Returns:
            bool: True if the write operation was successful, False otherwise.
        """
        writer = PLCWriter(self.client)
        return writer.write(address, value, data_type)

    def close(self):
        """
        Closes the connection to the PLC.

        This method should be called when the PLC object is no longer needed.
        """
        if self.client.get_connected():
            self.client.disconnect()
        self.client.destroy()
