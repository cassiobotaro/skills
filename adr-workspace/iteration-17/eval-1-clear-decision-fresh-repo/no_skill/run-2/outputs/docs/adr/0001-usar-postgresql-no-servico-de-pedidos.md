# ADR 0001: Usar PostgreSQL no serviço de pedidos

- **Status:** Aceita
- **Data:** 2026-11-22

## Contexto

O serviço de pedidos precisa de um banco de dados principal. As opções consideradas foram PostgreSQL e MongoDB.

O fluxo de criação de pedido atualiza estoque, pagamento e pedido ao mesmo tempo. Essas atualizações precisam ser atômicas: se qualquer uma falhar, nenhuma pode ser aplicada. Isso exige transações ACID.

Além disso, o time já tem experiência com PostgreSQL, e a empresa já paga por uma infraestrutura RDS.

## Decisão

Usaremos **PostgreSQL** como banco de dados do serviço de pedidos. A criação de pedido executará as atualizações de estoque, pagamento e pedido em uma única transação.

## Alternativas consideradas

### MongoDB

Não foi escolhido. O motivo principal é o requisito de transação ACID entre estoque, pagamento e pedido. A experiência do time com Postgres e o RDS já contratado também pesaram contra.

## Consequências

### Positivas

- Transações ACID cobrem todo o fluxo de criação de pedido, sem compensações manuais.
- O time já conhece a tecnologia, o que reduz a curva de aprendizado e o risco operacional.
- Aproveita o RDS que a empresa já paga, sem novo fornecedor ou custo de plataforma.

### Negativas

- O schema é mais rígido. Mudanças no modelo de dados exigem planejamento.
- Migrações de schema passam a ser um passo explícito do deploy, e precisam ser coordenadas com a publicação da aplicação.
