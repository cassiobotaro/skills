Registrei a decisão como ADR 3, com status `Accepted` e data 2026-11-22. O arquivo é `doc/adr/0003-use-redis-for-user-session-cache.md`.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês. Escrevi o título e o texto em inglês para manter o log consistente, e não em português. Se preferir o log em português, eu traduzo.
- **Conteúdo:**
  - **Context:** os dois motivos que você deu, tirar carga de leitura do PostgreSQL e ter expiração automática das chaves.
  - **Decision:** "We will use Redis…", em vez de guardar as sessões no PostgreSQL.
  - **Consequences:** o ganho (menos leitura no banco principal e expiração automática) e o trade-off aceito. O trade-off tem duas partes: mais um componente de infraestrutura para operar, e as sessões se perdem se o Redis reiniciar sem persistência.
- **Outros ADRs:** nenhum foi alterado. O ADR 2 (PostgreSQL) continua válido, porque ele trata da persistência principal do serviço, não das sessões.
