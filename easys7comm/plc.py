import snap7
from snap7.util import get_int, set_int
from easys7comm import PLCReader, DataType, PLCWriter

class PLC:
    def __init__(self, ip: str, rack: int = 0, slot: int = 1):
        """
        Initializes a PLC object with the given IP, rack, and slot.
        """
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()
        self.client.connect(self.ip, self.rack, self.slot)

    def read(self, address: str, data_type: DataType):
        """
        Reads a block of data from the PLC.
        """
        reader = PLCReader(self.client)
        return reader.read(address, data_type)
    

    def write(self, address: str, value, data_type: DataType):
        """
        Writes a block of data to the PLC.
        """
        writer = PLCWriter(self.client)
        return writer.write(address, value, data_type)
        

    def close(self):
        """
        Closes the connection to the PLC.
        """
        self.client.disconnect()
        self.client.destroy()

# Example usage
if __name__ == "__main__":
    plc = PLC("10.254.176.81")
    try:
        print("Leitura Bool:")
        print("Leitura Byte:", plc.read("DB20.DBB1", DataType.BYTE))
        print("Leitura Int:", plc.read("DB20.DBW2", DataType.INT))
        print("Leitura String:", plc.read("DB20.DBX12.0", DataType.STRING))
        print("Escrita: Bool")
        print("Escrita: ", plc.write("DB20.DBB1", 2, DataType.BYTE))
        print("Escrita: ", plc.write("DB20.DBW2", 321, DataType.INT))
        print("Escrita: ", plc.write("DB20.DBX12.0", "Marum", DataType.STRING))
    finally:
        plc.close()
