import snap7
from snap7 import util

from .plc_parse_address import PlcParseAddress
from .plc_types import DataType


class PLCWriter:
    def __init__(self, plc):
        self.plc = plc

    def parse_value(self, value, data_type: DataType, *, bit: int | None = None) -> bytearray:
        bytearray_ = bytearray(data_type.size)
        if data_type.method_set_name is None:
            raise ValueError(f"Data type {data_type.name} is read-only and cannot be written")

        setter = getattr(util, data_type.method_set_name)
        if data_type == DataType.BOOL:
            setter(bytearray_, 0, bit or 0, value)
        else:
            setter(bytearray_, 0, value)
        return bytearray_

    def write_db_value(self, db_number, offset_byte, value):
        self.plc.db_write(db_number, offset_byte, value)

    def write_area_value(self, area: int, offset: int, value: bytearray):
        self.plc.write_area(area, 0, offset, value)

    def write(self, address: str, value, data_type: DataType):
        address_info = PlcParseAddress.parse_address(address)

        if address_info["address_category"] == "DB":
            return self.write_db_value(
                address_info["db"],
                address_info["byte_offset"],
                self.parse_value(value, data_type, bit=address_info.get("bit")),
            )

        area_map = {
            "M": snap7.type.Areas.MK,
            "I": snap7.type.Areas.PE,
            "Q": snap7.type.Areas.PA,
        }

        if address_info["address_category"] in area_map:
            return self.write_area_value(
                area_map[address_info["address_category"]],
                address_info["address"],
                self.parse_value(value, data_type, bit=address_info.get("bit")),
            )

        raise NotImplementedError(f"Address type '{address_info['address_category']}' is not supported.")
