Escrevi o ADR da decisão e, como o repositório não tinha log, criei também um ADR 0001 inicial.

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md` é o ADR inicial padrão do adr-tools ("registrar decisões de arquitetura"), traduzido para português. Ele abre o log, e a sua decisão ficou como 0002.
- `doc/adr/0002-usar-postgresql-em-vez-de-mongodb-no-servi-o-de-pedidos.md` registra a decisão com status `Accepted` e data 2026-11-22.
  - **Contexto:** o fluxo de criação de pedido atualiza estoque, pagamento e pedido juntos e precisa de transação ACID. O time já tem experiência com Postgres e a empresa já paga o RDS.
  - **Decisão:** usar PostgreSQL no serviço de pedidos, em vez de MongoDB.
  - **Consequências:** a criação de pedido passa a ser uma única transação ACID. O custo é um schema mais rígido e migrações como passo de deploy.

Só usei os motivos e a desvantagem que você descreveu e não acrescentei nada. A prosa está em português. Os rótulos que o adr-tools lê (`Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences` e `Accepted`) ficaram em inglês, para o `adr` e o `!adrs` do Structurizr conseguirem lê-los. Por isso o acento sumiu do nome dos arquivos (`decis-es`, `servi-o`) e continua nos títulos dentro deles.

Não fiz commit.
