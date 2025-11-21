# Guia do Usuário (Engenheiros e Técnicos)

## O que o EasyS7Comm resolve
- Ler e escrever valores no CLP sem estudar Snap7 ou bytes.
- Usar endereços Siemens do jeito que você já usa no TIA Portal (DBW, DBX, DBD).
- Ter exemplos prontos para copiar e colar em scripts de teste ou em HMIs simples.

## Conexão passo a passo
1. Instale Python 3.10+.
2. Instale o pacote:
   ```bash
   pip install easys7comm python-snap7
   ```
3. Confirme que o CLP responde ao ping:
   ```bash
   ping 192.168.0.10
   ```
4. Teste a conexão:
   ```python
   from easys7comm import S7Client

   client = S7Client("192.168.0.10")
   client.connect()
   print("Conectado!", client.read_bool("M0.0"))
   client.disconnect()
   ```
