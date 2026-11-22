Escrevi o ADR da decisão e criei o log de ADRs do repositório, que estava vazio. Não rodei nenhuma ferramenta de ADR (`adr list` etc.) para validar os arquivos.

Arquivos criados:
- `doc/adr/0001-registrar-decis-es-de-arquitetura.md`: ADR inicial padrão do adr-tools ("registrar decisões de arquitetura"), traduzido para português. Ele abre o log, e a sua decisão virou o 0002.
- `doc/adr/0002-usar-postgresql-em-vez-de-mongodb-no-servi-o-de-pedidos.md`: o ADR da decisão, com status `Accepted` e data 2026-11-22.

O que está no ADR 0002:
- **Contexto:** o fluxo de criação de pedido atualiza estoque, pagamento e pedido juntos e precisa de uma transação ACID. O time já conhece PostgreSQL e a empresa já paga o RDS.
- **Decisão:** usar PostgreSQL, no RDS, no serviço de pedidos, em vez de MongoDB.
- **Consequências:** a criação de pedido fica numa única transação, o time usa tecnologia que conhece e o RDS já está pago. Em troca, o schema fica mais rígido e as migrações viram um passo do deploy.

O texto está em português, como a conversa. Os rótulos `Date:`, `## Status`, `## Context`, `## Decision` e `## Consequences` e a palavra `Accepted` ficaram em inglês, porque o adr-tools e o importador `!adrs` do Structurizr leem esses termos exatos. Por isso o nome do arquivo também perde os acentos (`servi-o`).

Só usei o que você me contou, sem acrescentar motivos nem alternativas. Se quiser registrar outra alternativa que o time avaliou além do MongoDB, ou outro risco, me diga e eu incluo.
