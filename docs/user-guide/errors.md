# Problemas comuns e troubleshooting

## Erros frequentes
- **IP errado**: confirme com `ping` ou `arp -a`.
- **Porta bloqueada (102)**: valide firewall da célula e regras de TI/OT.
- **Firewall industrial**: muitas células têm ACL específica; peça liberação do mestre para a sua estação.
- **Timeout**: rede lenta ou cabo ruim. Teste um `read_bool("M0.0")` curto para validar.
- **DB otimizado ligado**: para acessar via Snap7, desative otimização de DB ou crie tags de acesso compatíveis.

## Checklist rápido
1. O CLP responde a `ping`?
2. Rack e slot estão corretos (geralmente 0 e 1)?
3. Porta 102 liberada?
4. Endereço está no formato Siemens (`DB1.DBW0`, `Q0.0`)?
5. Teste um ponto simples (ex.: `M0.0`) antes de ler um array grande.
6. Persistem falhas? Reinicie a conexão com `disconnect()` e `connect()`.
