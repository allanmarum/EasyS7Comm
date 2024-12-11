import snap7
from snap7.util import get_bool, get_int, get_real

class Snap7Client:
    def __init__(self, ip: str, rack: int = 0, slot: int = 1):
        """
        Inicializa o cliente Snap7.
        
        :param ip: Endereço IP do CLP.
        :param rack: Rack do CLP.
        :param slot: Slot do CLP.
        """
        self.client = snap7.client.Client()
        self.ip = ip
        self.rack = rack
        self.slot = slot

    def connect(self):
        """Conecta ao CLP."""
        try:
            self.client.connect(self.ip, self.rack, self.slot)
            if self.client.get_connected():
                print(f"Conectado ao CLP: {self.ip}")
        except Exception as e:
            print(f"Erro ao conectar ao CLP: {e}")
            raise

    def disconnect(self):
        """Desconecta do CLP."""
        if self.client.get_connected():
            self.client.disconnect()
            print("Desconectado do CLP")

    def read_db(self, db_number: int, start: int, size: int) -> bytes:
        """
        Lê dados de uma área de dados (DB) do CLP.
        
        :param db_number: Número do DB a ser lido.
        :param start: Posição inicial dentro do DB.
        :param size: Quantidade de bytes a ser lida.
        :return: Bytes lidos do DB.
        """
        try:
            pass
        except Exception as e:
            print(f"Erro ao ler DB {db_number}: {e}")
            raise

    def write_db(self, db_number: int, start: int, data: bytes):
        """
        Escreve dados em uma área de dados (DB) do CLP.
        
        :param db_number: Número do DB a ser escrito.
        :param start: Posição inicial dentro do DB.
        :param data: Dados a serem escritos.
        """
        try:
            pass
        except Exception as e:
            print(f"Erro ao escrever no DB {db_number}: {e}")
            raise

    def read_bool(self, db_number: int, start: int, bit: int) -> bool:
        """
        Lê um bit específico de um DB.
        
        :param db_number: Número do DB.
        :param start: Byte de início.
        :param bit: Bit dentro do byte.
        :return: Valor booleano do bit.
        """
        data = self.read_db(db_number, start, 1)
        return get_bool(data, 0, bit)

    def read_int(self, db_number: int, start: int) -> int:
        """
        Lê um valor inteiro (2 bytes) de um DB.
        
        :param db_number: Número do DB.
        :param start: Byte de início.
        :return: Valor inteiro lido.
        """
        data = self.read_db(db_number, start, 2)
        return get_int(data, 0)

    def read_real(self, db_number: int, start: int) -> float:
        """
        Lê um valor float (4 bytes) de um DB.
        
        :param db_number: Número do DB.
        :param start: Byte de início.
        :return: Valor float lido.
        """
        data = self.read_db(db_number, start, 4)
        return get_real(data, 0)
