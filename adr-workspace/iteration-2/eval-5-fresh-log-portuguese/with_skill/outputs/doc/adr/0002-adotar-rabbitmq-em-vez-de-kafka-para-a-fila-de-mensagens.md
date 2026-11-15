# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Date: 2026-06-07

## Status

Aceito

## Contexto

Os serviços precisam se comunicar de forma assíncrona por meio de uma fila de mensagens, e é necessário escolher a tecnologia que cumprirá esse papel. As duas opções consideradas são o RabbitMQ e o Kafka.

A equipe já possui experiência operacional com RabbitMQ. O volume de mensagens é baixo, abaixo de 100 mensagens por segundo. A retenção de eventos não é um requisito: não precisamos manter o histórico de mensagens para releitura posterior.

O Kafka oferece retenção de eventos e a capacidade de reprocessá-los (replay), recursos que pesam a seu favor quando há essa necessidade, mas que vêm acompanhados de maior complexidade operacional.

## Decisão

Vamos adotar o RabbitMQ como fila de mensagens para a comunicação assíncrona entre os serviços.

## Consequências

A operação se apoia na experiência que a equipe já tem com RabbitMQ, reduzindo o risco e a curva de aprendizado em comparação com a adoção do Kafka.

Para o volume atual, abaixo de 100 mensagens por segundo, o RabbitMQ atende com folga, sem a complexidade operacional adicional do Kafka.

Abrimos mão da retenção de eventos e da capacidade de reprocessá-los (replay). Se no futuro o replay de eventos passar a ser necessário, isso será objeto de uma nova decisão, eventualmente revisando ou substituindo esta.
