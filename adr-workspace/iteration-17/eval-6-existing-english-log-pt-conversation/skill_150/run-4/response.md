Registrei a decisão como ADR 3, com status `Accepted` e a data de hoje (2026-11-22): `doc/adr/0003-use-redis-for-user-session-cache.md`.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log num único idioma. Se preferir o log em português, posso traduzir, mas aí o ideal é migrar todos os registros.
- **Contexto e decisão:** o motivo é tirar a carga de leitura do PostgreSQL e ter expiração automática das chaves. Decidimos usar Redis em vez de guardar as sessões no PostgreSQL.
- **Consequências:** coloquei os dois ganhos e os dois trade-offs que você descreveu. Os trade-offs são mais um componente de infraestrutura para operar e a perda das sessões se o Redis reiniciar sem persistência.
- **ADR 2:** não o marquei como superseded nem emendado. Ele trata do PostgreSQL como persistência principal do serviço e não menciona sessões, então continua valendo.
- **Não inventei nada:** não acrescentei alternativas, números nem motivos que você não tenha dado.
