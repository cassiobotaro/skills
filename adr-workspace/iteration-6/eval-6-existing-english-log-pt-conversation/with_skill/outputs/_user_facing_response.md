Registrei a decisão como ADR 3 no log existente em `doc/adr/`.

**Arquivo criado:** `doc/adr/0003-use-redis-for-user-session-storage.md`

```markdown
# 3. Use Redis for user session storage

Date: 2026-07-21

## Status

Accepted

## Context

User sessions were going to be kept in PostgreSQL, the primary store chosen in ADR 2.
Session lookups happen on every authenticated request, so they add read load to the same
database that serves the transactional workload. Sessions also have a natural lifetime
and need to expire on their own, which PostgreSQL does not provide without an extra
cleanup mechanism.

## Decision

We will store user sessions in Redis instead of PostgreSQL, relying on Redis key
expiration to retire sessions automatically.

## Consequences

Read load is taken off the primary database: session lookups no longer compete with the
transactional workload.

Session expiration is handled by Redis key TTLs, so no cleanup job is needed.

We take on one more piece of infrastructure to operate, monitor, and keep available.

Sessions are lost if Redis restarts without persistence, which means users are logged
out.
```

Duas observações:

- **Escrevi o ADR em inglês**, mesmo com a nossa conversa em português, porque o log
  existente (`0001-record-architecture-decisions.md` e `0002-use-postgresql-for-persistence.md`)
  está todo em inglês — um log em duas línguas fica pior do que em qualquer uma delas.
  Se você preferir passar o log para português, dá para fazer, mas aí vale converter os
  ADRs antigos junto.
- **Não marquei o ADR 2 como substituído.** Ele decide o PostgreSQL como persistência
  primária do serviço, o que continua valendo; esta decisão só tira as sessões de lá.
  Se você considera que ela emenda o ADR 2, eu adiciono o par `Amends` / `Amended by`
  nas duas seções de Status.
