Como o repositório ainda não tinha nenhum ADR, criei o log em `doc/adr/` (o padrão do adr-tools) e o inicializei com o ADR semente antes de registrar a sua decisão.

Arquivos criados:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` — o ADR semente, que registra a própria decisão de manter um log de decisões de arquitetura neste projeto.
- `doc/adr/0002-usar-postgresql-em-vez-de-mongodb-no-servico-de-pedidos.md` — a sua decisão, com status `Accepted`.

O ADR 2 ficou assim: o Context descreve o fluxo de criação de pedido atualizando estoque, pagamento e pedido juntos com necessidade de transação ACID, mais a experiência do time com Postgres e o RDS já pago; o Decision diz que vamos usar PostgreSQL em vez de MongoDB; e o Consequences lista tanto os ganhos quanto o custo aceito — schema mais rígido e migrações virando um passo de deploy.

O texto está em português, mas o "esqueleto" que as ferramentas leem (o rótulo `Date:`, os quatro títulos `## Status` / `## Context` / `## Decision` / `## Consequences` e a palavra de status `Accepted`) fica em inglês, que é o formato canônico do adr-tools.
