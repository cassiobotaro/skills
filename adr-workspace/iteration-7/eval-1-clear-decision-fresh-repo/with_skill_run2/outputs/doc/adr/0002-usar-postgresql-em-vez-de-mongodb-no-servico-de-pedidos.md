# 2. Usar PostgreSQL em vez de MongoDB no serviço de pedidos

Date: 2026-07-21

## Status

Accepted

## Context

O fluxo de criação de pedido do serviço de pedidos atualiza estoque, pagamento e pedido em conjunto. Essas atualizações precisam acontecer como uma única unidade: ou todas valem, ou nenhuma vale. Isso exige transação ACID abrangendo as três escritas.

O MongoDB era a outra opção considerada para o armazenamento do serviço.

Dois fatores do contexto da empresa também pesam na escolha: o time já tem experiência com PostgreSQL, e a empresa já paga pelo RDS.

## Decision

Vamos usar PostgreSQL como banco de dados do serviço de pedidos.

## Consequences

A criação de pedido passa a poder atualizar estoque, pagamento e pedido dentro de uma transação ACID, então uma falha no meio do fluxo não deixa os três em estados inconsistentes.

O time trabalha com uma tecnologia que já conhece, e a operação se apoia no RDS que a empresa já contrata — sem custo novo de infraestrutura nem de aprendizado.

Em contrapartida, o schema fica mais rígido: mudanças na forma dos dados precisam ser declaradas antecipadamente, e não acomodadas documento a documento.

Migrações passam a ser um passo de deploy. Toda alteração de schema vira uma etapa a ser escrita, revisada e executada junto com a entrega, o que torna o deploy mais pesado e exige cuidado com compatibilidade entre versões da aplicação e do banco.
