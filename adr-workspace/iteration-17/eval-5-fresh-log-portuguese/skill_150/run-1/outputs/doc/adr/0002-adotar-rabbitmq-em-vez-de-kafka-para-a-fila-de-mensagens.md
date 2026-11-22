# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Date: 2026-11-22

## Status

Accepted

## Context

Os serviços precisam de uma fila de mensagens para se comunicar entre si. A equipe já tem experiência operacional com RabbitMQ. O volume é baixo, menos de 100 mensagens por segundo, e não precisamos de retenção de eventos.

## Decision

Vamos adotar o RabbitMQ, e não o Kafka, como fila de mensagens entre os serviços.

## Consequences

Abrimos mão do replay de eventos. Se um dia precisarmos dele, será uma nova decisão.

A operação se apoia na experiência que a equipe já tem com RabbitMQ.
