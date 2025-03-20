# easys7comm/plc_types.py

"""
PLC Data Types Module

This module defines the `DataType` enumeration, which maps common PLC data 
types to their corresponding getter and setter methods, along with their 
memory sizes in bytes.

These types are used for reading and writing data from and to a PLC.
"""

from enum import Enum


class DataType(Enum):
    """
    Enum representing different PLC data types.

    Each data type includes:
        - The method name for reading (getter)
        - The method name for writing (setter)
        - The memory size in bytes
    """

    BOOL    = ("get_bool",   "set_bool",   1)
    BYTE    = ("get_byte",   "set_byte",   1)
    WORD    = ("get_word",   "set_word",   2)
    DWORD   = ("get_dword",  "set_dword",  4)
    INT     = ("get_int",    "set_int",    2)
    DINT    = ("get_dint",   "set_dint",   4)
    UINT    = ("get_uint",   "set_uint",   2)
    UDINT   = ("get_udint",  "set_udint",  4)
    REAL    = ("get_real",   "set_real",   4)
    LREAL   = ("get_lreal",  "set_lreal",  8)
    CHAR    = ("get_char",   None,         1)   # No setter available
    STRING  = ("get_string", "set_string", 254)  # Default max size
    FS_STRING = ("get_fstring", "set_fstring", 254)  # Fixed-size string
    TIME    = ("get_time",   "set_time",   4)
    DATE    = (None,         "set_date",   2)   # No getter available
    USINT   = ("get_usint",  "set_usint",  1)
    SINT    = ("get_sint",   "set_sint",   1)
    WCHAR   = ("get_wchar",  None,         2)   # No setter available
    WSTRING = ("get_wstring", None,        508)  # Wide string

    def __init__(self, method_get_name: str, method_set_name: str, size: int):
        """
        Initialize a DataType enum member.

        Args:
            method_get_name (str or None): The method name for reading the value.
            method_set_name (str or None): The method name for writing the value.
            size (int): The memory size of the data type in bytes.
        """
        self.method_get_name = method_get_name
        self.method_set_name = method_set_name
        self.size = size
