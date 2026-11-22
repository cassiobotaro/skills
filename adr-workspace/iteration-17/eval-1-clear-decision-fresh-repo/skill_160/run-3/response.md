Escrevi o ADR da decisão e criei o log de ADRs, porque o repositório não tinha nenhum. Não rodei `adr list` nem outra ferramenta para validar os arquivos.

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md` é o ADR inicial, o mesmo que o `adr init` cria ("Registrar decisões de arquitetura"). Traduzi para português, como o resto do log.
- `doc/adr/0002-usar-postgresql-em-vez-de-mongodb-no-servi-o-de-pedidos.md` é o ADR do PostgreSQL, com status `Accepted` e data 2026-11-22.

O Context traz só o que você disse: o fluxo que atualiza estoque, pagamento e pedido numa transação ACID, a experiência do time com Postgres e o RDS que a empresa já paga. A Decision é "Vamos usar PostgreSQL, no RDS, … em vez de MongoDB". As Consequences listam os ganhos e o custo que você citou, o schema mais rígido e as migrações como passo de deploy.

Os títulos e o texto estão em português. O `Date:`, os cabeçalhos `## Status`, `## Context`, `## Decision` e `## Consequences` e a palavra `Accepted` ficam em inglês, que é o formato que o adr-tools e o `!adrs` do Structurizr leem. Por isso os nomes dos arquivos perdem os acentos (`decis-es`, `servi-o`), e os títulos dentro dos arquivos mantêm.

Se o ADR ainda aguarda aprovação de alguém, troque o status para `Proposed`.
