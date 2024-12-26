import snap7
from snap7 import util
from enum import Enum

class DataType(Enum):
    BOOL = ("get_bool", "set_bool", 1)
    BYTE = ("get_byte", "set_byte", 1)
    WORD = ("get_word", "set_word", 2)
    DWORD = ("get_dword", "set_dword", 4)
    INT = ("get_int", "set_int", 2)
    DINT = ("get_dint", "set_dint", 4)
    UINT = ("get_uint", "set_uint", 2)
    UDINT = ("get_udint", "set_udint", 4)
    REAL = ("get_real", "set_real", 4)
    LREAL = ("get_lreal", "set_lreal", 8)
    CHAR = ("get_char", None, 1)  # No corresponding `set_char` function
    STRING = ("get_string", "set_string", 256)  # Default size
    FS_STRING = ("get_fstring", "set_fstring", 256)  # Fixed string size
    TIME = ("get_time", "set_time", 4)
    DATE = (None, "set_date", 2)  # No corresponding `get_date` function
    USINT = ("get_usint", "set_usint", 1)
    SINT = ("get_sint", "set_sint", 1)
    WCHAR = ("get_wchar", None, 2)  # No corresponding `set_wchar` function
    WSTRING = ("get_wstring", None, 512)  # Wide string, assuming a default size

    def __init__(self, method_get_name, method_set_name, size):
        self.method_get_name = method_get_name
        self.method_set_name = method_set_name
        self.size = size

class PLCInterface:
    
    def __init__(self, ip_address: str, rack: int, slot: int, port: int=102):
        self.client = snap7.client.Client()
        self.client.connect(ip_address, rack, slot, port)
        self.client.get_connected()
        pass
    
    def read_db_row(self, db_number: int, offset_byte: int, data_type: 'DataType'):
        data = self.client.db_read(db_number, offset_byte, data_type.size)
        get_function = getattr(util, data_type.method_get_name, None)
        return get_function(data, 0)
    
    def disconnect(self):
        if self.client.get_connected():
            self.client.disconnect()
    
    
if __name__ == "__main__":
    plc = PLCInterface("10.254.176.88", 0, 1)
    data =  plc.read_db_row(7, 6, DataType.STRING)
    print(data)
    plc.disconnect()
