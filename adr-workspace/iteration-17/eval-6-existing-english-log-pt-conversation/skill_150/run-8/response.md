Registrei a decisão como ADR 3, com status `Accepted`: `doc/adr/0003-use-redis-for-user-session-cache.md`.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log consistente. Os rótulos (`Date:`, `## Status` e os outros) ficam em inglês de qualquer forma, porque o adr-tools e o importador do Structurizr leem esses literais.
- **Context:** contém só o que você disse. As sessões ficariam no PostgreSQL, o que aumenta a carga de leitura no banco principal, e queremos expiração automática das chaves.
- **Consequences:** registrei os dois ganhos (menos leitura no banco principal e expiração automática) e os dois trade-offs que você aceitou (mais um componente para operar e perda das sessões se o Redis reiniciar sem persistência).
- **Alternativas:** não inventei nenhuma além do PostgreSQL.
- **Supersede:** o ADR 2 trata de PostgreSQL como persistência principal e continua valendo. Por isso não houve supersede e nenhum arquivo existente foi alterado.

Se vocês consideraram outras alternativas, como Memcached, ou já decidiram habilitar persistência no Redis, me diga. Acrescento ao registro.
