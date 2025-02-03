# easys7comm/plc_writer.py
"""
PLC Writer Module

This module provides the PLCWriter class for writing data to a PLC.
"""

from snap7 import util
from .plc_connection import PLCConnection
from .plc_types import DataType  # Assumes DataType is defined in your types module


class PLCWriter(PLCConnection):
    """
    PLCWriter class for writing data to the PLC.

    Inherits from PLCConnection to reuse connection logic.
    """
    def write_db_row(self, db_number: int, offset_byte: int, value: any, data_type: DataType) -> None:
        """
        Write a value to a PLC datablock at the specified offset using the provided data type.

        Args:
            db_number (int): The datablock number.
            offset_byte (int): The starting byte offset within the datablock.
            value (any): The value to write.
            data_type (DataType): An instance containing information about the data type,
                                  including the size and the snap7 set method name.

        Raises:
            ValueError: If the appropriate write method is not available for the data type.
        """
        if data_type.method_set_name is None:
            raise ValueError(f"Write method not available for data type '{data_type.name}'.")

        set_function = getattr(util, data_type.method_set_name, None)
        if not callable(set_function):
            raise ValueError(f"Write method '{data_type.method_set_name}' not found in snap7.util.")

        # Prepare a byte array of the appropriate size.
        data_bytes = bytearray(data_type.size)
        set_function(data_bytes, 0, value)
        # Write the data to the PLC datablock.
        self.client.db_write(db_number, offset_byte, data_bytes)