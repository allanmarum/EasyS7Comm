import snap7
from snap7 import util

from .plc_parse_address import PlcParseAddress
from .plc_types import DataType


class PLCReader:
    """Low-level read helpers backed by a Snap7 client."""

    def __init__(self, plc):
        """Initialize the reader with a Snap7 client instance.

        Args:
            plc: Snap7 client used to issue read operations.
        """

        self.plc = plc

    def parse_value(self, raw_data: bytearray, data_type: DataType, *, bit: int | None = None):
        """Translate raw PLC bytes into a Python value.

        Args:
            raw_data: Raw bytes returned from Snap7.
            data_type: Expected :class:`DataType` to extract.
            bit: Bit offset for boolean values.

        Returns:
            Parsed Python value corresponding to ``data_type``.
        """

        getter = getattr(util, data_type.method_get_name)
        if data_type == DataType.BOOL:
            return getter(raw_data, 0, bit or 0)
        return getter(raw_data, 0)

    def read_db_row(self, db_number: int, offset: int, data_type: DataType, *, bit: int | None = None):
        """Read from a DB area and parse the result."""

        data = self.plc.db_read(db_number, offset, data_type.size)
        return self.parse_value(data, data_type, bit=bit)

    def read_area(self, area: int, offset: int, data_type: DataType, *, bit: int | None = None):
        """Read from a process image (I/Q/M) area and parse the result."""

        data = self.plc.read_area(area, 0, offset, data_type.size)
        return self.parse_value(data, data_type, bit=bit)

    def read(self, address: str, data_type: DataType):
        """Read a value from the PLC using a generic address string.

        Args:
            address: PLC memory address, e.g. ``"DB1.DBD0"`` or ``"M10.0"``.
            data_type: :class:`DataType` describing how to parse the value.

        Returns:
            Parsed Python value.

        Raises:
            NotImplementedError: If the address area is unsupported.
        """

        info = PlcParseAddress.parse_address(address)

        if info["address_category"] == "DB":
            return self.read_db_row(info["db"], info["byte_offset"], data_type, bit=info.get("bit"))

        area_map = {
            "M": snap7.type.Areas.MK,
            "I": snap7.type.Areas.PE,
            "Q": snap7.type.Areas.PA,
        }

        if info["address_category"] in area_map:
            return self.read_area(area_map[info["address_category"]], info["address"], data_type, bit=info.get("bit"))

        raise NotImplementedError(f"Address type '{info['address_category']}' is not supported.")
