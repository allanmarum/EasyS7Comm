# EasyS7Comm – Documentação Técnica

## Introdução
EasyS7Comm é um wrapper Python que abstrai o Snap7 e oferece uma API simples para leitura e escrita em CLPs Siemens. Ele padroniza o endereçamento, centraliza o tratamento de erros e expõe métodos prontos para uso direto em projetos industriais.

### Problema que resolve
- Configuração manual e repetitiva do Snap7 em cada projeto.
- Conversões de tipos e offsets de memória propensos a erro.
- Falta de fluxos prontos para reconexão, timeout e troubleshooting.

### Snap7 vs. EasyS7Comm
| Aspecto | Snap7 | EasyS7Comm |
| --- | --- | --- |
| API | Baixo nível, foco em blocos e áreas | Alto nível, métodos como `read_int` e `write_bool` |
| Endereçamento | Exige cálculos de offset | Usa endereços Siemens (ex.: `DB1.DBW0`) |
| Tratamento de erros | Delega ao usuário | Exceções semânticas (`S7CommunicationError`, `S7AddressError`) |
| Documentação | Focada em C/PLC | Guias práticos para Python |

### Principais vantagens
- Interface Pythonic com métodos específicos por tipo.
- Parsing automático de endereços Siemens.
- Base preparada para uso em serviços web (Flask/FastAPI) ou integrações MQTT.
- Docstrings em Google Style + referência automática via mkdocstrings.

### Requisitos
- Python 3.10+
- Snap7 instalado no sistema (biblioteca nativa + pacote Python `python-snap7`).
- Plataformas testadas: Linux (Ubuntu/Debian) e contêiner Docker base Debian. Windows é suportado instalando o Snap7 correspondente.

## Estrutura interna para quem quer contribuir

### Layout do projeto
```
easys7comm/
    __init__.py
    client.py
    exceptions.py
    plc.py
    plc_connection.py
    plc_parse_address.py
    plc_reader.py
    plc_types.py
    plc_writer.py
```

### Principais módulos
- `client.S7Client`: interface de alto nível com métodos de leitura e escrita por tipo.
- `plc.PLC`: encapsula o cliente Snap7 bruto.
- `plc_reader` / `plc_writer`: conversão de bytes <-> tipos Python.
- `plc_parse_address`: validação e decomposição de endereços Siemens.
- `exceptions`: hierarquia de erros específica do domínio.

### Fluxo de conexão
1. `S7Client.connect()` cria a sessão Snap7 (rack/slot/porta).
2. Leitura/escrita delega para `PLCReader`/`PLCWriter` que validam endereços.
3. Operações retornam tipos Python ou disparam exceções semânticas.
4. `disconnect()` fecha e libera o cliente.

### Conversão de tipos
- `DataType` mapeia métodos `snap7.util` (get/set) e tamanho em bytes.
- `PLCReader.parse_value` e `PLCWriter.parse_value` aplicam os getters/setters apropriados.

### Como adicionar novos métodos de leitura/escrita
1. Adicione o tipo em `plc_types.DataType` com getter/setter e tamanho.
2. Crie métodos convenientes em `S7Client` (ex.: `read_time`) chamando `_read`/`_write` com o novo `DataType`.
3. Atualize o guia rápido e exemplos avançados na documentação.

## Tratamento de erros e boas práticas
- Capture `S7CommunicationError` para falhas de rede ou sessão.
- Valide endereços com `PlcParseAddress.parse_address` e trate `S7AddressError`.
- Configure timeouts do Snap7 conforme a rede (ex.: `client.set_connection_params`).
- Reconecte em loops de automação longa (estratégia de backoff exponencial sugerida).
- Pooling: crie uma instância do `S7Client` por célula de máquina e reutilize-a; evite reconectar por ciclo.

## Exemplos avançados
### Leitura de array
```python
addresses = [f"DB10.DBW{2*i}" for i in range(10)]
values = [client.read_int(addr) for addr in addresses]
```

### Escrita de booleans
```python
client.write_bool("Q0.0", True)
client.write_bool("M10.3", False)
```

### Uso com FastAPI
```python
from fastapi import FastAPI, HTTPException
from easys7comm import S7Client, S7CommunicationError

client = S7Client("192.168.0.10", auto_connect=True)
api = FastAPI()

@api.get("/status")
def status():
    try:
        return {"running": client.read_bool("M0.0")}
    except S7CommunicationError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
```

### Execução em thread
```python
import threading
from easys7comm import S7Client

client = S7Client("192.168.0.10", auto_connect=True)

def worker():
    temperature = client.read_real("DB1.DBD4")
    print("T:", temperature)

threading.Thread(target=worker, daemon=True).start()
```

### Integração com MQTT
```python
import json
import paho.mqtt.client as mqtt
from easys7comm import S7Client

client = S7Client("192.168.0.10", auto_connect=True)
mqttc = mqtt.Client()
mqttc.connect("broker", 1883)

payload = {"speed": client.read_int("DB1.DBW0")}
mqttc.publish("plc/data", json.dumps(payload))
```
