import snap7
from snap7 import util

from .plc_parse_address import PlcParseAddress
from .plc_types import DataType


class PLCWriter:
    """Low-level write helpers backed by a Snap7 client."""

    def __init__(self, plc):
        """Initialize the writer with a Snap7 client instance.

        Args:
            plc: Snap7 client used to issue write operations.
        """

        self.plc = plc

    def parse_value(self, value, data_type: DataType, *, bit: int | None = None) -> bytearray:
        """Convert a Python value into a PLC byte representation.

        Args:
            value: Python value to convert.
            data_type: :class:`DataType` describing how to encode the value.
            bit: Bit offset for boolean values.

        Returns:
            A ``bytearray`` ready to be written to the PLC.

        Raises:
            ValueError: If the ``data_type`` cannot be written.
        """

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
        """Write bytes directly to a DB area."""

        self.plc.db_write(db_number, offset_byte, value)

    def write_area_value(self, area: int, offset: int, value: bytearray):
        """Write bytes directly to a process image (I/Q/M) area."""

        self.plc.write_area(area, 0, offset, value)

    def write(self, address: str, value, data_type: DataType):
        """Write a value to the PLC using a generic address string.

        Args:
            address: PLC memory address, e.g. ``"DB1.DBD0"`` or ``"M10.0"``.
            value: Python value to write.
            data_type: :class:`DataType` describing how to encode ``value``.

        Returns:
            None

        Raises:
            NotImplementedError: If the address area is unsupported.
        """

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
