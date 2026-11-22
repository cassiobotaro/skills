Escrevi o ADR da decisão e criei o log de ADRs, já que o repositório não tinha nenhum. Não rodei nenhuma ferramenta de ADR sobre os arquivos.

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md` é o ADR inicial padrão do `adr init`, que registra que o projeto passa a usar ADRs. Traduzi o título e o corpo para português.
- `doc/adr/0002-usar-postgresql-em-vez-de-mongodb-no-servi-o-de-pedidos.md` é o ADR da decisão, com status `Accepted`.

O ADR 0002 usa só o que você me contou:
- **Contexto:** o fluxo de criação de pedido atualiza estoque, pagamento e pedido juntos e precisa de transação ACID. O time já conhece Postgres e a empresa já paga o RDS. As opções consideradas foram PostgreSQL e MongoDB.
- **Decisão:** usar PostgreSQL em vez de MongoDB no serviço de pedidos.
- **Consequências:** a criação de pedido roda numa única transação ACID, e o time e o RDS são aproveitados. Em contrapartida, o schema fica mais rígido e as migrações viram um passo do deploy.

Os títulos e os textos estão em português, mas mantive em inglês `Date:`, os cabeçalhos `## Status/Context/Decision/Consequences` e `Accepted`. O adr-tools e o `!adrs` do Structurizr leem esses termos exatamente assim. Os nomes dos arquivos perdem os acentos, por exemplo `servi-o`. Os títulos dentro dos arquivos continuam acentuados.

A data nos dois arquivos é 2026-11-22.

Marquei como `Accepted` porque você disse que a decisão já foi tomada. Se ainda falta alguém concordar, troque para `Proposed`.
