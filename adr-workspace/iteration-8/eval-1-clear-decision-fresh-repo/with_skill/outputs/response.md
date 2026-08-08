Como o repositório ainda não tinha nenhum ADR, iniciei o log de decisões em `doc/adr/` (o diretório padrão do adr-tools) e criei dois arquivos:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` — o ADR inicial padrão, que registra a própria decisão de manter um log de decisões de arquitetura. É o equivalente ao `adr init`; ele existe para que o ADR 2 não fique sem a decisão que o justifica.
- `doc/adr/0002-usar-postgresql-em-vez-de-mongodb-no-servico-de-pedidos.md` — a decisão que você descreveu.

O ADR 2 ficou com status `Accepted` e registra exatamente o que você trouxe: no Context, a necessidade de transação ACID no fluxo que atualiza estoque, pagamento e pedido juntos, mais a experiência do time com Postgres e o RDS que a empresa já paga; no Decision, o uso do PostgreSQL em vez do MongoDB; e nas Consequences, tanto os ganhos quanto as duas desvantagens que vocês discutiram — schema mais rígido e migrações como passo de deploy.

Uma observação sobre o formato: a prosa está em português, mas o andaime que as ferramentas leem (o rótulo `Date:`, os quatro títulos `## Status` / `## Context` / `## Decision` / `## Consequences` e a palavra de status `Accepted`) fica em inglês de propósito. É assim que o adr-tools emite e é isso que o importador de decisões do Structurizr procura; traduzir esses literais faria a data e o status serem silenciosamente ignorados.

Se em algum momento essa decisão for revista, o caminho é escrever um ADR novo que a substitua (`Supersedes`), não editar o 0002 — o valor do log está em preservar o que *era* a decisão.
