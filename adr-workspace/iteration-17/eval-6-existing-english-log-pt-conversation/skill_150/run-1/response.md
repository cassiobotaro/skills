Registrei a decisão como ADR 3 e criei `doc/adr/0003-use-redis-for-user-session-cache.md`. Nenhum outro arquivo foi alterado.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log consistente. Posso traduzir se você preferir.
- **Status e data:** `Accepted`, com a data de hoje (2026-11-22).
- **Contexto:** guarda só o que você me disse. As sessões poderiam ficar no PostgreSQL, o que aumenta a carga de leitura no banco principal, e ali a expiração precisaria de outro mecanismo.
- **Decisão:** "We will use Redis as the cache for user sessions, instead of storing sessions in PostgreSQL."
- **Consequências:**
  - Positivas: menos leitura no banco principal e expiração automática das chaves.
  - Negativas: mais um componente de infraestrutura para operar e perda das sessões se o Redis reiniciar sem persistência.
- **Supersede:** não marquei nenhum ADR como superseded. O ADR 2 trata da persistência geral no PostgreSQL e não menciona sessões, então continua valendo.
