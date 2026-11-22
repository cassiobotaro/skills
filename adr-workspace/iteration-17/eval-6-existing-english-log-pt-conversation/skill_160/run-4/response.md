Registrei a decisão como ADR 3, em `doc/adr/0003-use-redis-for-user-session-cache.md`, com status `Accepted` e data 2026-11-22.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log num idioma só. Se preferir, posso traduzir.
- **Contexto e decisão:** o contexto traz só os motivos que você deu: tirar carga de leitura do PostgreSQL principal e ter expiração automática das chaves. A decisão é "We will use Redis as the cache for user sessions, instead of storing them in PostgreSQL."
- **Consequências:** registrei o benefício (sem leituras de sessão no banco principal e com expiração automática) e os dois trade-offs que você aceitou. São mais um componente de infraestrutura para operar e a perda das sessões se o Redis reiniciar sem persistência.
- **Outros ADRs:** não alterei nenhum. O ADR 2 trata do PostgreSQL como persistência principal e continua valendo, então não há supersede nem amend.
