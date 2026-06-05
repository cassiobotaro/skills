# 2. Usar PostgreSQL como banco de dados

Date: 2025-11-17

## Status

Accepted

## Context

O sistema de faturamento precisa de um banco relacional com suporte a transações, consultas analíticas moderadas e bom suporte do time de infraestrutura. O time já opera PostgreSQL em outros produtos.

## Decision

Usaremos PostgreSQL como banco de dados principal do sistema de faturamento, tanto para dados transacionais quanto para o status de processamento das faturas.

## Consequences

O time aproveita o conhecimento operacional existente. Caso a carga analítica cresça, será necessário avaliar réplicas de leitura ou um banco analítico dedicado (nova decisão).
