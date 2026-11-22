Registrei a decisão como ADR 3, com status `Accepted`, em `doc/adr/0003-use-redis-for-user-session-cache.md`.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então o título e o texto do ADR 3 também estão em inglês, para o log não ficar com dois idiomas. Os rótulos (`Date:`, `## Status`, `## Context` etc.) ficam em inglês de qualquer forma, porque o adr-tools e o `!adrs` do Structurizr dependem deles.
- **Contexto:** a carga de leitura das sessões no banco principal e a expiração automática das chaves.
- **Decisão:** usar Redis para o cache de sessões, em vez do PostgreSQL.
- **Consequências:** menos leitura no banco principal e expiração automática. Em contrapartida, há mais um componente de infraestrutura para operar. As sessões também se perdem se o Redis reiniciar sem persistência, e o texto registra que isso foi aceito.
- **Sem supersede:** o ADR 2 trata do PostgreSQL como persistência principal do serviço, e essa decisão continua valendo. Por isso não alterei nenhum ADR existente.

Não registrei alternativas além do PostgreSQL, nem detalhes como o modo de persistência do Redis, porque você não os mencionou. Se quiser incluí-los, me passe e eu ajusto o texto.
