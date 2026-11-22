Criei o ADR em `docs/adr/0001-usar-postgresql-no-servico-de-pedidos.md`. Como o repositório não tinha nenhum ADR, escolhi o diretório `docs/adr/` e a numeração `0001`. Se você preferir outro local ou formato, é só dizer.

O documento tem status **Aceito**, data de hoje (2026-11-22) e as seções Contexto, Decisão, Consequências e Alternativas consideradas. Registrei o seguinte:

- **Motivos:** transação ACID no fluxo que atualiza estoque, pagamento e pedido, experiência do time com Postgres e o RDS que a empresa já paga.
- **Desvantagens:** schema mais rígido e migrações como passo de deploy.

Na seção sobre o MongoDB, escrevi que o time tem "menos experiência" com ele e que não há infraestrutura contratada para ele. Você não disse isso com essas palavras. Eu deduzi a partir da experiência com Postgres e do RDS existente, então confirme se está correto.

Não fiz commit.
