# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Date: 2026-06-07

## Status

Accepted

## Context

Os serviços precisam de uma fila de mensagens para se comunicar entre si. O volume de tráfego é baixo, abaixo de 100 mensagens por segundo, e não há necessidade de reter os eventos para reprocessamento posterior. A equipe já possui experiência operacional com RabbitMQ. As principais opções consideradas foram RabbitMQ e Kafka.

## Decision

Vamos adotar o RabbitMQ como fila de mensagens entre os serviços, em vez do Kafka.

## Consequences

A operação fica mais simples por se apoiar na experiência que a equipe já tem com RabbitMQ, sem o custo de aprender e operar o Kafka.

Abrimos mão do replay de eventos, já que o RabbitMQ não retém os eventos da forma que o Kafka faz. Se um dia precisarmos de retenção e reprocessamento de eventos, isso será objeto de uma nova decisão.
