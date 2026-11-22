Registrei a decisão como ADR 3, em `doc/adr/0003-use-redis-for-user-session-caching.md`, com status `Accepted` e data 2026-11-22.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log num idioma só. Se preferir o log em português, traduzo.
- **Conteúdo:** só usei o que você disse.
  - **Contexto:** a carga de leitura no banco principal e a expiração automática das chaves.
  - **Decisão:** Redis em vez de PostgreSQL para as sessões.
  - **Consequências:** o alívio de leitura no banco e a expiração automática, mais os dois trade-offs que você aceitou (mais um componente para operar e perda das sessões se o Redis reiniciar sem persistência).
- **Sem supersede:** o ADR 2 (PostgreSQL para persistência) continua válido, porque ele trata do armazenamento principal e não de sessões. Por isso não alterei nenhum ADR existente.
