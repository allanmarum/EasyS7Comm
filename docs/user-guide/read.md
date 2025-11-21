# Ler valores rapidamente

## Inteiro (DBW)
```python
valor = client.read_int("DB1.DBW0")
```

## Real (DBD)
```python
temperatura = client.read_real("DB1.DBD4")
```

## Bool (DBX / M / I / Q)
```python
motor_ligado = client.read_bool("DB1.DBX0.0")
entrada = client.read_bool("I0.1")
saida = client.read_bool("Q4.2")
merker = client.read_bool("M10.3")
```

## Bloco de bytes (DBB)
```python
pacote = client.read_bytes("DB20.DBB0", length=8)
print(pacote)
```

## Array simples
```python
enderecos = [f"DB10.DBW{2*i}" for i in range(5)]
leituras = [client.read_int(addr) for addr in enderecos]
print(leituras)
```
