# 2. Usar PostgreSQL em vez de MongoDB no serviço de pedidos

Date: 2026-08-07

## Status

Accepted

## Context

O fluxo de criação de pedido do serviço de pedidos atualiza estoque, pagamento e pedido em conjunto. Essas três escritas precisam acontecer como uma única transação ACID.

As opções consideradas foram PostgreSQL e MongoDB.

O time já tem experiência com PostgreSQL e a empresa já paga por RDS.

## Decision

Vamos usar PostgreSQL como banco de dados do serviço de pedidos, em vez de MongoDB.

## Consequences

A atualização de estoque, pagamento e pedido passa a acontecer dentro de uma transação ACID, sem que o serviço precise coordenar consistência por conta própria.

O time trabalha com uma tecnologia que já conhece, e a operação se apoia no RDS que a empresa já paga.

Em troca, o schema fica mais rígido: mudanças de modelo exigem alteração explícita do banco.

As migrações passam a ser um passo do deploy, o que acrescenta uma etapa ao processo de publicação do serviço.
