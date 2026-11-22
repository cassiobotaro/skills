# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Date: 2026-11-22

## Status

Accepted

## Context

Os serviços precisam trocar mensagens por meio de uma fila. A equipe já tem experiência operacional com RabbitMQ, o volume é baixo (menos de 100 mensagens por segundo) e não precisamos de retenção de eventos.

## Decision

Vamos adotar o RabbitMQ, e não o Kafka, como fila de mensagens entre os serviços.

## Consequences

Abrimos mão do replay de eventos. Se um dia precisarmos disso, será uma nova decisão.

A operação se apoia na experiência que a equipe já tem com RabbitMQ.
