Escrevi o ADR da decisão e criei os arquivos no repositório. Não rodei nenhuma ferramenta de ADR sobre eles.

Como o repositório não tinha nenhum ADR, criei o log em `doc/adr/`, que é o padrão do adr-tools. Ele começa com um ADR 0001 de abertura, que é o registro padrão "Registrar decisões de arquitetura", traduzido para português. A sua decisão ficou como 0002.

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md`
- `doc/adr/0002-usar-postgresql-em-vez-de-mongodb-no-servi-o-de-pedidos.md`

O 0002 está com status `Accepted` e data 2026-11-22.

- **Context:** a criação de pedido atualiza estoque, pagamento e pedido juntos e precisa de transação ACID. O time já conhece PostgreSQL e a empresa já paga o RDS.
- **Decision:** vamos usar PostgreSQL, no RDS, no serviço de pedidos, em vez de MongoDB.
- **Consequences:** os benefícios são a transação única e o aproveitamento da experiência do time e do RDS. Os custos são o schema mais rígido e as migrações como passo de deploy.

Usei só o que você descreveu e não acrescentei motivos nem alternativas além do MongoDB.

Os nomes dos arquivos não têm acentos (por exemplo, `servi-o`). O adr-tools gera o nome assim, e os títulos dentro dos arquivos continuam acentuados. O texto está em português, mas `Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences` e `Accepted` ficaram em inglês, porque as ferramentas de ADR esperam esses termos exatos.

Se quiser outra pasta, como `docs/adr`, é só avisar que eu movo os arquivos e crio o `.adr-dir`.
