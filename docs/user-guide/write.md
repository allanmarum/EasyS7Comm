# Escrever valores

## Inteiro (DBW)
```python
client.write_int("DB1.DBW0", 123)
```

## Real (DBD)
```python
client.write_real("DB1.DBD4", 45.6)
```

## Bool (DBX / M / I / Q)
```python
client.write_bool("DB1.DBX0.0", True)
client.write_bool("Q0.0", False)
client.write_bool("M10.3", True)
```

## Bloco de bytes (DBB)
```python
client.write_bytes("DB20.DBB0", b"\x01\x02\x03\x04")
```

## Escrevendo múltiplos valores
```python
enderecos = ["DB10.DBW0", "DB10.DBW2", "DB10.DBW4"]
valores = [10, 20, 30]
for addr, val in zip(enderecos, valores):
    client.write_int(addr, val)
```
