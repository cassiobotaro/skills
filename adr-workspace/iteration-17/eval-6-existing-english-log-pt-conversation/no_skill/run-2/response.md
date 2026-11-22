Registrei a decisão como o ADR 0003, em `doc/adr/0003-use-redis-for-session-cache.md`. Segui o formato dos ADRs existentes (Nygard), que estão em inglês, então o texto também está em inglês.

- **Status:** Accepted, com data de 2026-11-22.
- **Relação com o ADR 0002:** o texto diz que o ADR complementa o 0002, sem substituí-lo. O PostgreSQL continua sendo o armazenamento principal, só as sessões ficam fora dele.
- **Contexto e decisão:** as sessões são lidas quase a cada requisição, o que pesa no banco principal. Com Redis, a expiração fica por conta do TTL das chaves.
- **Consequências:** menos carga de leitura no PostgreSQL e expiração automática. Em contrapartida, há mais um componente para operar e as sessões se perdem se o Redis reiniciar sem persistência.

Não fiz commit. Se quiser, posso fazer.
