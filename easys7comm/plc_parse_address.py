import re

from .plc_types import DataType


class PlcParseAddress:
    """Parser for Siemens-style PLC address strings."""

    @staticmethod
    def parse_address(addr: str):
        """Parse a Siemens address into its components.

        Args:
            addr: Address string such as ``"DB1.DBW0"`` or ``"M10.0"``.

        Returns:
            A dictionary containing the parsed components.

        Raises:
            ValueError: If the address format is invalid or missing bits where required.
        """

        if addr.upper().startswith("DB"):
            m = re.match(r"DB(\d+)\.([A-Za-z]+)(\d+)(?:\.(\d+))?", addr, re.IGNORECASE)
            if m:
                db = int(m.group(1))
                typ = m.group(2).upper()
                byte_offset = int(m.group(3))
                bit = int(m.group(4)) if m.group(4) is not None else None
                if typ == "DBX" and bit is None:
                    raise ValueError(f"Bit value required for DBX address: {addr}")
                if typ != "DBX" and bit is not None:
                    raise ValueError(f"Unexpected bit value for {typ}: {addr}")
                return {
                    "address_category": "DB",
                    "db": db,
                    "addr_type": typ,
                    "byte_offset": byte_offset,
                    "bit": bit,
                }
            raise ValueError(f"Invalid DB address format: {addr}")

        m = re.match(r"^([MIQ])(\d+)(?:\.(\d+))?$", addr, re.IGNORECASE)
        if m:
            return {
                "address_category": m.group(1).upper(),
                "address": int(m.group(2)),
                "bit": int(m.group(3)) if m.group(3) is not None else None,
            }
        raise ValueError(f"Invalid address format: {addr}")
