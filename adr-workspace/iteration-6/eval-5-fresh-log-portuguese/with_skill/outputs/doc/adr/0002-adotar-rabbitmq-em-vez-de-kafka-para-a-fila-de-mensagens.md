# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Date: 2026-07-21

## Status

Accepted

## Context

Os serviços precisam trocar mensagens entre si por meio de uma fila. As duas opções consideradas foram RabbitMQ e Kafka.

O volume de mensagens é baixo: menos de 100 mensagens por segundo. Não há necessidade de retenção de eventos.

A equipe já tem experiência operacional com RabbitMQ.

## Decision

Vamos adotar o RabbitMQ como fila de mensagens entre os serviços.

## Consequences

A operação se apoia na experiência que a equipe já tem com RabbitMQ.

Abrimos mão do replay de eventos, que o Kafka ofereceria pela retenção do log. Se um dia precisarmos dessa capacidade, ela será objeto de uma nova decisão.
