Como o repositório ainda não tinha nenhum ADR, inicializei o log de decisões em `doc/adr/` (equivalente ao `adr init`) e registrei a decisão. Como nossa conversa é em português, o log já começa em português.

Arquivos criados:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` — o ADR semente, que registra a própria decisão de adotar Architecture Decision Records (Michael Nygard / adr-tools). É o ponto de partida padrão de todo log de ADRs.
- `doc/adr/0002-usar-postgresql-no-servico-de-pedidos.md` — a decisão de usar PostgreSQL em vez de MongoDB no serviço de pedidos.

O ADR 0002 documenta:

- **Contexto**: o fluxo de criação de pedido atualiza estoque, pagamento e pedido juntos e precisa de consistência entre as três escritas (transação ACID); o time já tem experiência com Postgres e a empresa já paga RDS.
- **Decisão**: "Usaremos PostgreSQL como banco de dados do serviço de pedidos, em vez do MongoDB", com as três escritas dentro de uma única transação ACID.
- **Consequências**: além dos ganhos (transação ACID, experiência do time, RDS já pago), registrei as duas desvantagens que vocês discutiram — o schema fica mais rígido e as migrações de schema passam a ser um passo do deploy.

Marquei o status como **Aceito**, partindo do entendimento de que a decisão já foi tomada. Se ela ainda estiver em discussão e aguardando aval de alguém, me avise que troco para **Proposto**.

Os arquivos seguem o formato adr-tools (numeração sequencial `NNNN-slug.md`), então ferramentas como `adr list` e o importador `!adrs` do Structurizr funcionam diretamente sobre eles.
