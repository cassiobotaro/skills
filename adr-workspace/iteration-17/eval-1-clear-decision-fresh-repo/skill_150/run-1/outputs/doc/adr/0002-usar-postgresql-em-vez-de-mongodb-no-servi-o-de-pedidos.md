# 2. Usar PostgreSQL em vez de MongoDB no serviço de pedidos

Date: 2026-11-22

## Status

Accepted

## Context

O fluxo de criação de pedido atualiza estoque, pagamento e pedido juntos e precisa de transação ACID.

O time já tem experiência com PostgreSQL, e a empresa já paga pelo RDS.

## Decision

Vamos usar PostgreSQL, no RDS, como banco de dados do serviço de pedidos, em vez de MongoDB.

## Consequences

A criação de pedido pode atualizar estoque, pagamento e pedido numa única transação ACID.

O time trabalha com uma tecnologia que já conhece, e a empresa aproveita o RDS que já paga.

O schema fica mais rígido do que ficaria com MongoDB.

As migrações de schema passam a ser um passo do deploy.
