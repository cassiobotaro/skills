Pronto. O repositório ainda não tinha nenhum log de decisões, então inicializei um do zero seguindo a convenção do adr-tools.

Arquivos criados:

- `doc/adr/0001-record-architecture-decisions.md` — ADR inicial padrão (o "seed"), que registra que o projeto passa a usar ADRs. É gerado automaticamente ao iniciar um log e fica como a decisão número 1.
- `doc/adr/0002-use-postgresql-for-the-orders-service.md` — a sua decisão: usar PostgreSQL em vez de MongoDB no serviço de pedidos.

O ADR 0002 documenta:

- **Context**: o fluxo de criação de pedido atualiza estoque, pagamento e pedido como uma unidade só e precisa de transação ACID; o time já opera Postgres e a empresa já paga RDS; o MongoDB foi a alternativa considerada.
- **Decision**: usar PostgreSQL no RDS existente, em vez de MongoDB.
- **Consequences**: ganho de transação ACID e reaproveitamento de experiência/RDS já pagos; e os trade-offs que vocês discutiram — schema mais rígido e migrações que viram um passo do deploy.

Os arquivos estão em formato adr-tools puro, então a sua tooling funciona neles direto: `adr list`, `adr generate toc`, `adr generate graph` e o importador `!adrs doc/adr` do Structurizr.

Escrevi os arquivos em inglês de propósito (cabeçalhos e corpo) — é a convenção dos ADRs e o que as ferramentas que fazem parse esperam, independente do idioma da conversa. Se preferir em português, é só avisar.
