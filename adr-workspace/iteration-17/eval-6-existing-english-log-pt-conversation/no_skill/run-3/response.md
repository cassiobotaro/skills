Registrei a decisão como o ADR 3, em `doc/adr/0003-use-redis-for-session-cache.md`. Segui o formato dos ADRs existentes (Nygard), com status "Accepted" e data de hoje, 2026-11-22. Escrevi o texto em inglês, como os ADRs 1 e 2.

- **Contexto:** as sessões são lidas em quase toda requisição, e guardá-las no PostgreSQL sobrecarrega o banco principal.
- **Decisão:** as sessões ficam no Redis, com expiração automática por TTL. O PostgreSQL continua como persistência principal para o resto, e o ADR 2 não foi substituído.
- **Consequências:** tirei a carga de leitura do banco e dispensei um job de limpeza de sessões. O trade-off aceito também está registrado: mais um componente para operar, e as sessões se perdem se o Redis reiniciar sem persistência, então os usuários precisam logar de novo.

Não fiz commit.
