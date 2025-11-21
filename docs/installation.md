# Instalação

## Instalando o pacote Python
```bash
pip install easys7comm
```

## Instalando o Snap7
A biblioteca nativa do Snap7 precisa estar disponível no sistema, além do pacote Python `python-snap7`.

### Windows
1. Baixe o binário do Snap7 correspondente à sua arquitetura em <https://sourceforge.net/projects/snap7/>.
2. Extraia e adicione o diretório `bin` ao `PATH` (arquivos `snap7.dll`).
3. Instale o pacote Python:
   ```bash
   pip install python-snap7
   ```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update && sudo apt-get install -y build-essential
wget https://sourceforge.net/projects/snap7/files/latest/download -O snap7.zip
unzip snap7.zip -d snap7 && cd snap7/build/unix
make -j$(nproc)
sudo make install
pip install python-snap7
```

### Docker
Para imagens base Debian/Ubuntu:
```Dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y build-essential wget unzip \
    && rm -rf /var/lib/apt/lists/*
RUN wget https://sourceforge.net/projects/snap7/files/latest/download -O snap7.zip \
    && unzip snap7.zip -d /tmp/snap7 \
    && cd /tmp/snap7/build/unix && make -j$(nproc) && make install
RUN pip install easys7comm python-snap7
```

## Verificando a conexão
```python
from easys7comm import S7Client

client = S7Client("192.168.0.10")
try:
    client.connect()
    print("Conectado!", client.read_bool("M0.0"))
finally:
    client.disconnect()
```
Se ocorrer falha de conexão, valide IP, rack/slot e firewall industrial.
