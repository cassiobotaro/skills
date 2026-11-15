# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Data: 2026-06-07

## Status

Aceito

## Contexto

Os serviços precisam trocar mensagens de forma assíncrona por meio de uma fila de mensagens. Duas tecnologias estavam em consideração: RabbitMQ e Kafka.

A equipe já possui experiência operacional com RabbitMQ. O volume de mensagens é baixo, abaixo de 100 mensagens por segundo. Não há necessidade de retenção de eventos para esse fluxo.

## Decisão

Adotaremos o RabbitMQ, em vez do Kafka, como fila de mensagens para a troca de mensagens entre os serviços.

## Consequências

Aproveitamos a experiência operacional que a equipe já tem com RabbitMQ, reduzindo o risco e o esforço de operação.

O RabbitMQ atende confortavelmente ao volume atual, abaixo de 100 mensagens por segundo, sem necessidade da retenção de eventos oferecida pelo Kafka.

Abrimos mão do replay de eventos. Se um dia precisarmos dessa capacidade, isso será objeto de uma nova decisão.
