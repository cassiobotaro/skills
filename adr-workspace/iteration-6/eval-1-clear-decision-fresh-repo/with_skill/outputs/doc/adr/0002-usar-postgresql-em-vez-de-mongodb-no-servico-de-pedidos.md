# 2. Usar PostgreSQL em vez de MongoDB no serviço de pedidos

Date: 2026-07-21

## Status

Accepted

## Context

O fluxo de criação de pedido do nosso serviço de pedidos atualiza estoque, pagamento e pedido em conjunto, e essas atualizações precisam acontecer dentro de uma única transação ACID.

O time já tem experiência com PostgreSQL, e a empresa já paga por RDS. As duas opções consideradas para o armazenamento do serviço foram PostgreSQL e MongoDB.

## Decision

Vamos usar PostgreSQL como banco de dados do serviço de pedidos, em vez de MongoDB.

## Consequences

A criação de pedido passa a poder atualizar estoque, pagamento e pedido em uma única transação ACID, sem precisar de compensações na aplicação.

Aproveitamos a experiência que o time já tem com PostgreSQL e a assinatura de RDS que a empresa já paga.

Em troca, o schema fica mais rígido: mudanças no modelo de dados exigem migrações, e as migrações passam a ser um passo do deploy.
