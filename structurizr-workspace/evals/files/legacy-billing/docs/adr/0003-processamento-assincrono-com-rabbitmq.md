# 3. Processamento assíncrono com RabbitMQ

Date: 2025-12-02

## Status

Accepted

## Context

A emissão de faturas dispara integrações lentas com o ERP corporativo. Processar tudo de forma síncrona na API degrada o tempo de resposta do portal e acopla a disponibilidade da API à do ERP.

## Decision

A API publica faturas emitidas em uma fila RabbitMQ e um worker dedicado consome a fila, processa a fatura e integra com o ERP de forma assíncrona.

## Consequences

O portal responde rápido mesmo com o ERP indisponível. Em contrapartida, passamos a ter consistência eventual no status das faturas e precisamos monitorar a fila (profundidade, DLQ e reprocessamento).
