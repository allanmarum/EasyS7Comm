import snap7
from snap7.util import get_int, set_int

class PLCInterface:
    def __init__(self, ip, rack, slot):
        self.client = snap7.client.Client()
        self.client.connect(ip, rack, slot)

    def read_data(self, db_number, start, size):
        """Read data from the PLC."""
        data = self.client.db_read(db_number, start, size)
        return data

    def write_data(self, db_number, start, data):
        """Write data to the PLC."""
        self.client.db_write(db_number, start, data)

    def close(self):
        """Close the connection to the PLC."""
        self.client.disconnect()
