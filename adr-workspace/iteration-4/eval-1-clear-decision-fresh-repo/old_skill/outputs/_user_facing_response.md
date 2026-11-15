Pronto! Como o repositório ainda não tinha nenhum ADR, iniciei o log de decisões em `doc/adr/` (equivalente ao `adr init`) e registrei a decisão. Como nossa conversa é em português, escrevi todo o log em português.

Arquivos criados:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` — o ADR semente padrão, que registra a própria decisão de adotar Architecture Decision Records no projeto.
- `doc/adr/0002-usar-postgresql-no-servico-de-pedidos.md` — a decisão de usar PostgreSQL em vez de MongoDB no serviço de pedidos.

O ADR 0002 ficou assim:

- **Contexto**: o fluxo de criação de pedido atualiza estoque, pagamento e pedido em conjunto e precisa de transação ACID; o time já tem experiência com PostgreSQL; a empresa já paga RDS; as opções em discussão eram PostgreSQL e MongoDB.
- **Decisão**: vamos usar PostgreSQL como banco do serviço de pedidos, em vez de MongoDB.
- **Consequências**: atomicidade ACID entre as três escritas e reaproveitamento de experiência e do RDS existente; em contrapartida, o schema fica mais rígido e cada migração vira um passo do deploy.

Os arquivos seguem o formato do adr-tools (numeração sequencial `NNNN-slug.md`, formato Michael Nygard), então suas ferramentas existentes (`adr list`, importador do Structurizr etc.) funcionam neles sem alteração. Se quiser ajustar o título, marcar como Proposto em vez de Aceito, ou registrar outra decisão, é só avisar.
