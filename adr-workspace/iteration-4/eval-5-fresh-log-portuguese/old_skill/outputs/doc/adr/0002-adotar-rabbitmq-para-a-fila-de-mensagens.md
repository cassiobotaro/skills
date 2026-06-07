# 2. Adotar RabbitMQ para a fila de mensagens

Data: 2026-06-07

## Status

Aceito

## Contexto

Os serviços precisam trocar mensagens entre si por meio de uma fila, e é necessário escolher a tecnologia que vai suportar essa comunicação. As opções consideradas foram o RabbitMQ e o Kafka.

A equipe já possui experiência operacional com RabbitMQ. O volume de mensagens é baixo, abaixo de 100 mensagens por segundo. Não há necessidade de reter eventos para consumo posterior.

O Kafka oferece retenção de eventos e a possibilidade de reprocessá-los (replay), recursos que o RabbitMQ não fornece da mesma forma. Esses recursos não correspondem às necessidades atuais do projeto.

## Decisão

Vamos adotar o RabbitMQ como fila de mensagens entre os serviços.

## Consequências

A equipe opera a fila com a tecnologia que já conhece, sem o custo de aprender e sustentar o Kafka.

Para o volume atual, abaixo de 100 mensagens por segundo, o RabbitMQ atende sem necessidade da infraestrutura adicional que o Kafka exigiria.

Abrimos mão da retenção de eventos e do replay: uma mensagem consumida não pode ser reprocessada a partir da fila. Caso o replay de eventos venha a ser necessário no futuro, isso será objeto de uma nova decisão.
