# Guia Rápido

```python
from easys7comm import S7Client

client = S7Client('192.168.0.10')
client.connect()

value = client.read_int('DB1.DBW0')
client.write_int('DB1.DBW0', 123)

client.disconnect()
```

## Endereçamento
- Use o formato Siemens: `DB<number>.<tipo><offset>` (ex.: `DB1.DBW0`, `DB1.DBD4`).
- Áreas de processo: `I` (entradas), `Q` (saídas), `M` (merkers). Exemplos: `I0.0`, `Q4.1`, `M10.2`.
- Bits exigem o sufixo após o ponto (`.0` a `.7`).

## Leitura
- `read_int`, `read_real`, `read_bool`, `read_dint` retornam tipos Python já convertidos.
- Para bytes crus: `read_bytes('DB1.DBB0', length=8)`.

## Escrita
- Métodos equivalentes: `write_int`, `write_real`, `write_bool`, `write_dint`.
- Bytes crus: `write_bytes('DB1.DBB0', b'\x01\x02')`.

## Tratamento básico de erros
- Endereço inválido → `S7AddressError`.
- Falha de comunicação → `S7CommunicationError`.
- Recomenda-se encapsular operações em `try/except` e reconectar quando necessário.
