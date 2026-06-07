# 2. Usar PostgreSQL no serviço de pedidos

Data: 2026-06-07

## Status

Aceito

## Contexto

O serviço de pedidos precisa persistir os dados das operações de pedido. O fluxo de criação de pedido atualiza estoque, pagamento e o próprio pedido em conjunto, e essas atualizações precisam ser consistentes entre si: ou todas se concretizam, ou nenhuma. Isso exige transações ACID que abranjam as três escritas.

O time já tem experiência com PostgreSQL, e a empresa já paga pelo Amazon RDS, então a operação e o custo de um banco relacional já estão cobertos.

## Decisão

Usaremos PostgreSQL como banco de dados do serviço de pedidos, em vez do MongoDB. O fluxo de criação de pedido executará as atualizações de estoque, pagamento e pedido dentro de uma única transação ACID.

## Consequências

A criação de pedido passa a contar com transações ACID que cobrem estoque, pagamento e pedido em uma só transação, garantindo que as três escritas sejam confirmadas ou revertidas em conjunto.

Aproveitamos a experiência do time com PostgreSQL e a infraestrutura de RDS já paga pela empresa, sem introduzir um novo tipo de banco para operar.

O schema fica mais rígido: as estruturas das tabelas precisam ser definidas antecipadamente e cada mudança de estrutura exige uma migração.

As migrações de schema passam a ser um passo do deploy, o que adiciona uma etapa ao processo de entrega e precisa ser coordenado com as mudanças de código.
