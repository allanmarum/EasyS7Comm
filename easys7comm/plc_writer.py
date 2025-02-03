from snap7 import util
from .plc_types import DataType
from .utils.plc_parse_address import PlcParseAddress

class PLCWriter:
    def __init__(self, plc):
        self.plc = plc
        
    def parse_value(self, value, data_type: DataType) -> bytearray:
        bytearray_ = bytearray(data_type.size)
        setter = getattr(util, data_type.method_set_name)
        setter(bytearray_, 0, value)
        return bytearray_
    
    def write_db_value(self, db_number, offset_byte, size, value):
        self.plc.db_write(db_number, offset_byte, value)
        pass
    
    def write(self, address: str, value, data_type: DataType):
        address_info = PlcParseAddress.parse_address(address)
        if address_info['address_category'] == 'DB':
            self.write_db_value (
                address_info['db'], 
                address_info['byte_offset'], 
                data_type.size, 
                self.parse_value(value, data_type)
            )