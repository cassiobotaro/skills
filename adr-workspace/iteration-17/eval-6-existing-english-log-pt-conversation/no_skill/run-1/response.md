Registrei a decisão como ADR 0003 em `doc/adr/0003-use-redis-for-user-session-cache.md`. Segui o formato e o idioma (inglês) dos ADRs existentes. O status é Accepted e a data é 2026-11-22.

- **Contexto:** as sessões são lidas em quase toda requisição, o que sobrecarrega a leitura do PostgreSQL principal. A expiração também exigiria jobs de limpeza.
- **Decisão:** usar Redis para o cache de sessões, com expiração automática por TTL das chaves.
- **Consequências:**
  - A carga de leitura sai do banco principal.
  - As sessões expiram sozinhas, sem job de limpeza.
  - Temos mais um componente de infraestrutura para operar.
  - Se o Redis reiniciar sem persistência, as sessões se perdem e os usuários precisam logar de novo. Registrei esse risco como aceito.

Não marquei o ADR 0002 como substituído. O PostgreSQL continua sendo a persistência principal, e o ADR 0003 só traz uma nota de que o complementa. Não fiz commit.
