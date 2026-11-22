Não consegui escrever o ADR ainda. O repositório está vazio: não tem código, nenhuma menção ao Redis nem pasta de ADRs. Não quero inventar o contexto de uma decisão arquitetural.

Preciso destas informações:

1. **Substituto:** vamos trocar o Redis pelo quê (Memcached, Valkey, Dragonfly, Postgres, outro)?
2. **Motivo:** o que levou à troca (licença, custo, performance, operação, outro)?
3. **Uso atual do Redis:** cache, filas, sessões, pub/sub ou rate limiting?
4. **Alternativas consideradas:** quais outras opções foram avaliadas e descartadas?
5. **Formato e local:** prefere MADR ou Nygard, em português ou inglês, e em qual caminho (por exemplo `docs/adr/0001-trocar-redis.md`)?

Se preferir, passe só o substituto e o motivo. Eu escrevo um rascunho em português, no formato Nygard, em `docs/adr/0001-substituir-redis.md`, e você ajusta depois.
