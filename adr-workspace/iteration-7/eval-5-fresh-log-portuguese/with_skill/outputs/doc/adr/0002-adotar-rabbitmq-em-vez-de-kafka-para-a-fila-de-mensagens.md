# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Date: 2026-07-21

## Status

Accepted

## Context

Os serviços precisam de uma fila de mensagens para se comunicarem entre si, e havia duas opções em consideração: RabbitMQ e Kafka.

O volume de mensagens é baixo: menos de 100 mensagens por segundo. A equipe já tem experiência operacional com RabbitMQ. Não há necessidade de retenção de eventos.

## Decision

Vamos adotar o RabbitMQ como fila de mensagens entre os serviços.

## Consequences

A operação da fila se apoia na experiência que a equipe já tem com RabbitMQ, em vez de exigir o aprendizado de uma tecnologia nova.

Abrimos mão do replay de eventos. Como não há retenção, não é possível reprocessar mensagens já consumidas.

Se em algum momento o replay de eventos passar a ser necessário, isso será tratado como uma nova decisão, e não como uma extensão desta.
