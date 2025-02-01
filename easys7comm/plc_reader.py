# easys7comm/plc_reader.py
"""
PLC Reader Module

This module provides the PLCReader class for reading data from a PLC.
"""

from snap7 import util
from .plc_connection import PLCConnection
from .types import DataType  # Assumes DataType is defined in your types module


class PLCReader(PLCConnection):
    """
    PLCReader class for reading data from the PLC.

    Inherits from PLCConnection to reuse connection logic.
    """
    def read_db_row(self, db_number: int, offset_byte: int, data_type: DataType) -> any:
        """
        Read a row from a PLC datablock using the provided data type.

        Args:
            db_number (int): The datablock number.
            offset_byte (int): The starting byte offset within the datablock.
            data_type (DataType): An instance containing information about the data type,
                                  including the size and the snap7 get method name.

        Returns:
            The value read from the PLC datablock.

        Raises:
            ValueError: If the appropriate read method is not available for the data type.
        """
        # Read raw data from the PLC datablock.
        data = self.client.db_read(db_number, offset_byte, data_type.size)
        get_function = getattr(util, data_type.method_get_name, None)
        if not callable(get_function):
            raise ValueError(f"Read method not available for data type '{data_type.name}'.")
        return get_function(data, 0)

    # Future expansion:
    # def read_memory(self, address: int, data_type: DataType) -> any:
    #     pass
    #
    # def read_io(self, address: int, data_type: DataType) -> any:
    #     pass
