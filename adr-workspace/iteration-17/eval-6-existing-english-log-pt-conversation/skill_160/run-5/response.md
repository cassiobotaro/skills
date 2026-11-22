Registrei a decisão como ADR 3 em `doc/adr/0003-use-redis-for-user-session-cache.md`, com status `Accepted` e data 2026-11-22.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log consistente. Se preferir o ADR em português, posso reescrevê-lo. Os cabeçalhos (`Status`, `Context`, `Decision`, `Consequences`) ficam em inglês de qualquer forma, porque o adr-tools e o Structurizr dependem desses nomes.
- **Conteúdo:** usei só o que você informou.
  - **Contexto:** a carga de leitura no banco principal e a expiração automática das chaves.
  - **Decisão:** usar Redis para as sessões, em vez do PostgreSQL.
  - **Consequências:** menos leitura no PostgreSQL, expiração automática, mais um componente para operar, e sessões perdidas se o Redis reiniciar sem persistência (trade-off aceito).
- **Sem supersede:** o ADR 2 (PostgreSQL como persistência principal) continua válido, então não alterei nenhum arquivo existente.
