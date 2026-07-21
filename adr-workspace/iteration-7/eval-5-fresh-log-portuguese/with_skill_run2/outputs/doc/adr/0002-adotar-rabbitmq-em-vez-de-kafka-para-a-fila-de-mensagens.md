# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Date: 2026-07-21

## Status

Accepted

## Context

Os serviços precisam trocar mensagens entre si e é preciso escolher a tecnologia de fila que fará essa intermediação. As duas opções consideradas foram RabbitMQ e Kafka.

O volume de mensagens é baixo: menos de 100 mensagens por segundo. Não há necessidade de retenção de eventos.

A equipe já tem experiência operacional com RabbitMQ.

## Decision

Vamos adotar o RabbitMQ como fila de mensagens entre os serviços.

## Consequences

A operação da fila se apoia na experiência que a equipe já tem com RabbitMQ.

Abrimos mão do replay de eventos. Se um dia essa capacidade for necessária, será objeto de uma nova decisão.
