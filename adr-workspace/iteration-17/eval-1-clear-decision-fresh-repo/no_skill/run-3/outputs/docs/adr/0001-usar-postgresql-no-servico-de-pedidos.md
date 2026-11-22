# ADR-0001: Usar PostgreSQL (e não MongoDB) no serviço de pedidos

- **Status:** Aceito
- **Data:** 2026-11-22

## Contexto

O fluxo de criação de pedido atualiza estoque, pagamento e pedido de forma conjunta. Essas alterações precisam ser atômicas: ou todas são aplicadas, ou nenhuma. Isso exige transações ACID.

Além do requisito técnico, o time já tem experiência com PostgreSQL e a empresa já paga por uma instância no Amazon RDS.

As opções consideradas foram PostgreSQL e MongoDB.

## Decisão

Usaremos **PostgreSQL** como banco de dados do serviço de pedidos.

## Justificativa

- **Transações ACID:** estoque, pagamento e pedido são gravados na mesma transação, o que evita estados parciais, como estoque baixado sem pedido criado.
- **Experiência do time:** o time já conhece Postgres, o que reduz curva de aprendizado e risco operacional.
- **Custo e infraestrutura:** a empresa já paga RDS, então não há novo contrato nem nova plataforma para operar.

## Consequências

### Positivas

- Consistência forte no fluxo de criação de pedido, garantida pelo banco.
- Menos código de compensação ou reconciliação na aplicação.
- Aproveitamento da infraestrutura e do conhecimento existentes.

### Negativas

- **Schema mais rígido:** mudanças no modelo de dados exigem alteração explícita do schema, o que é menos flexível que o modelo de documentos do MongoDB.
- **Migrações no deploy:** migrações de schema passam a ser um passo do processo de deploy e precisam ser planejadas e versionadas junto com o código.

## Alternativa descartada

**MongoDB:** o schema flexível facilitaria a evolução do modelo. Foi descartado porque o fluxo central depende de transações ACID entre várias entidades. Além disso, o time tem menos experiência com a ferramenta e não há infraestrutura da empresa já contratada para ela.
