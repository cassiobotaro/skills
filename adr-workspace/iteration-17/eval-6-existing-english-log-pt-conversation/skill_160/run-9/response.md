Registrei a decisão como o ADR 3, em `doc/adr/0003-use-redis-for-user-session-cache.md`, com status `Accepted` e data 2026-11-22.

O texto está em inglês, não em português. Os ADRs 1 e 2 do log já são em inglês, e a skill manda manter o idioma do log. Os cabeçalhos (`Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences`) ficam em inglês de qualquer forma, para o adr-tools e o `!adrs` do Structurizr conseguirem ler o arquivo.

- **Context:** a alternativa era guardar as sessões no PostgreSQL. Queremos tirar a carga de leitura do banco principal e ter expiração automática das chaves.
- **Decision:** "We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL."
- **Consequences:**
  - Ganhamos menos leitura no banco principal e expiração automática das chaves.
  - Passamos a operar mais um componente de infraestrutura.
  - As sessões se perdem se o Redis reiniciar sem persistência. O ADR registra que aceitamos esse trade-off.

Só criei esse arquivo. O ADR 2 (PostgreSQL) continua válido, porque ele trata da persistência principal e não das sessões. Por isso não marquei nenhum ADR como substituído.
