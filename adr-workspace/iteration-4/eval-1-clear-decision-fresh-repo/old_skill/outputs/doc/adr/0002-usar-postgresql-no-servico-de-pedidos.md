# 2. Usar PostgreSQL no serviço de pedidos

Data: 2026-06-07

## Status

Aceito

## Contexto

O serviço de pedidos precisa de um banco de dados. O fluxo de criação de pedido atualiza estoque, pagamento e pedido em conjunto, e essas três escritas precisam acontecer de forma atômica, com garantias de transação ACID.

O time já tem experiência com PostgreSQL, e a empresa já paga por instâncias gerenciadas do Amazon RDS, sobre o qual o PostgreSQL pode rodar sem custo de infraestrutura adicional.

As opções em discussão eram PostgreSQL e MongoDB.

## Decisão

Vamos usar PostgreSQL como banco de dados do serviço de pedidos, em vez de MongoDB.

## Consequências

O fluxo de criação de pedido pode atualizar estoque, pagamento e pedido dentro de uma única transação ACID, garantindo atomicidade entre as três escritas.

A equipe aproveita a experiência que já tem com PostgreSQL, e a operação reaproveita o RDS que a empresa já paga, sem novo custo de infraestrutura.

Em contrapartida, o schema fica mais rígido: mudanças na estrutura dos dados exigem migrações explícitas, e cada migração passa a ser um passo do processo de deploy.
