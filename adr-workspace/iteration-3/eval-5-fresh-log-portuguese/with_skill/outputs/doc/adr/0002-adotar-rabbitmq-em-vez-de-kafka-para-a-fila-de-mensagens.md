# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Data: 2026-06-07

## Status

Aceito

## Contexto

Os serviços precisam trocar mensagens de forma assíncrona por meio de uma fila, e é necessário escolher a tecnologia que sustentará essa comunicação. Kafka e RabbitMQ são as duas opções consideradas.

A equipe já tem experiência operacional com RabbitMQ. O volume de mensagens é baixo — menos de 100 mensagens por segundo. A comunicação entre os serviços não exige retenção de eventos: as mensagens são consumidas e descartadas, sem necessidade de reprocessar o histórico.

## Decisão

Adotaremos o RabbitMQ como fila de mensagens entre os serviços.

## Consequências

Operamos sobre uma tecnologia que a equipe já conhece, reduzindo o risco operacional e a curva de aprendizado em comparação à adoção do Kafka.

Abrimos mão do replay de eventos. Como o RabbitMQ descarta as mensagens após o consumo e não retém o histórico, não será possível reprocessar eventos a partir de um ponto no passado. Se essa capacidade vier a ser necessária, será objeto de uma nova decisão.
