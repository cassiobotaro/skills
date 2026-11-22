Registrei a decisão como ADR 3, com status `Accepted`, em `doc/adr/0003-use-redis-for-user-session-cache.md`.

O log existente está em inglês, então escrevi o título e o texto em inglês para manter o padrão. Os cabeçalhos e o campo `Date:` ficam em inglês de qualquer forma, porque o adr-tools e o importador do Structurizr leem esses nomes.

- **Contexto:** a leitura de sessões no PostgreSQL pesaria no banco principal, e queremos expiração automática das chaves.
- **Decisão:** "We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL."
- **Consequências:** de bom, sai a carga de leitura do banco principal e as chaves expiram sozinhas. O custo aceito é mais um componente de infraestrutura para operar e a perda das sessões se o Redis reiniciar sem persistência.

Não alterei nenhum ADR existente. O ADR 2 trata do PostgreSQL como persistência principal do serviço, e essa decisão continua valendo.

Escrevi só o que você informou, sem acrescentar alternativas ou métricas. Se quiser registrar outras opções que foram consideradas, ou o plano de persistência do Redis, me diga que eu complemento.
