# 2. Usar PostgreSQL em vez de MongoDB no serviço de pedidos

Date: 2026-07-21

## Status

Accepted

## Context

O serviço de pedidos precisa de um banco de dados. As duas opções em discussão eram PostgreSQL e MongoDB.

O fluxo de criação de pedido atualiza estoque, pagamento e pedido em conjunto, e essas três atualizações precisam acontecer dentro de uma mesma transação ACID.

Além das características técnicas, dois fatores de contexto pesam na escolha: o time já tem experiência com Postgres, e a empresa já paga pelo RDS.

## Decision

Vamos usar PostgreSQL como banco de dados do serviço de pedidos, hospedado no RDS que a empresa já contrata.

## Consequences

O fluxo de criação de pedido pode atualizar estoque, pagamento e pedido em uma única transação ACID, sem que o serviço precise coordenar consistência entre as três escritas por conta própria.

O time trabalha com uma tecnologia que já conhece, e a decisão não acrescenta custo de infraestrutura, já que o RDS já é pago.

Em contrapartida, aceitamos um schema mais rígido: a estrutura dos dados passa a ser declarada explicitamente e mudanças nela deixam de ser livres.

Migrações passam a ser um passo de deploy. Toda alteração de schema precisa ser escrita, versionada e executada junto com a entrega, o que adiciona trabalho e um ponto de falha ao processo de release.
