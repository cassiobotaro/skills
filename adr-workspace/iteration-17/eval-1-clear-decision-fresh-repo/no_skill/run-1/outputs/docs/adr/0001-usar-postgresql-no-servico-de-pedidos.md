# ADR-0001: Usar PostgreSQL (e não MongoDB) no serviço de pedidos

- **Status:** Aceito
- **Data:** 2026-11-22

## Contexto

O serviço de pedidos precisa escolher seu banco de dados principal. As opções consideradas foram PostgreSQL e MongoDB.

O fluxo de criação de pedido atualiza **estoque, pagamento e pedido** juntos. Essas atualizações precisam ser atômicas: se uma falhar, nenhuma deve ser aplicada. Isso exige transações ACID.

Também pesaram:

- O time já tem experiência com PostgreSQL.
- A empresa já paga por uma instância no Amazon RDS.

## Decisão

Usaremos **PostgreSQL**, hospedado no **Amazon RDS**, como banco de dados do serviço de pedidos. O fluxo de criação de pedido executará as atualizações de estoque, pagamento e pedido em uma única transação.

## Consequências

### Positivas

- Garantia de atomicidade e consistência no fluxo de criação de pedido, sem compensações manuais na aplicação.
- Menor curva de aprendizado, já que o time conhece a tecnologia.
- Sem novo custo ou nova infraestrutura para operar, pois aproveita o RDS já contratado.

### Negativas / trade-offs

- **Schema mais rígido:** mudanças de modelo exigem alterar o schema explicitamente, o que é menos flexível que um banco de documentos.
- **Migrações viram um passo de deploy:** alterações de schema precisam ser versionadas e executadas como parte do processo de deploy, com coordenação entre a versão do código e a do schema.

## Alternativas consideradas

### MongoDB

Schema flexível, o que facilitaria a evolução do modelo. Foi descartado porque o fluxo central precisa de transações ACID entre estoque, pagamento e pedido. Além disso, o time tem menos experiência com ele e não há infraestrutura contratada para ele.
