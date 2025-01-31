# easys7comm/plc_interface.py

import snap7
from snap7 import util
from .types import DataType

class PLCInterface:
    def __init__(self, ip_address: str, rack: int, slot: int, port: int = 102):
        self.client = snap7.client.Client()
        self.client.connect(ip_address, rack, slot, port)
        if not self.client.get_connected():
            raise ConnectionError(f"Unable to connect to PLC at {ip_address}.")

    def read_db_row(self, db_number: int, offset_byte: int, data_type: DataType):
        data = self.client.db_read(db_number, offset_byte, data_type.size)
        get_function = getattr(util, data_type.method_get_name, None)
        if not callable(get_function):
            raise ValueError(f"Read method not available for data type {data_type.name}.")
        return get_function(data, 0)
        
    def write_db_row(self, db_number: int, offset_byte: int, value, data_type: DataType):
        if data_type.method_set_name is None:
            raise ValueError(f"Write method not available for data type {data_type.name}.")
        set_function = getattr(util, data_type.method_set_name, None)
        if not callable(set_function):
            raise ValueError(f"Write method {data_type.method_set_name} not found in snap7.util.")
        data_bytes = bytearray(data_type.size)
        set_function(data_bytes, 0, value)
        # Actually write the data to the PLC datablock
        self.client.db_write(db_number, offset_byte, data_bytes)
    
    def disconnect(self):
        if self.client.get_connected():
            self.client.disconnect()