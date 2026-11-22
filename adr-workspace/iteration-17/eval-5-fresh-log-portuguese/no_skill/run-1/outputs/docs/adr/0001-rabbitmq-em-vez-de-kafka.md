# ADR 0001: Adotar RabbitMQ em vez de Kafka para a fila de mensagens entre serviços

- **Status:** Aceita
- **Data:** 2026-11-22

## Contexto

Os serviços precisam trocar mensagens de forma assíncrona e é preciso escolher um broker. As opções consideradas foram RabbitMQ e Kafka.

Fatores relevantes:

- A equipe já tem experiência operacional com RabbitMQ.
- O volume é baixo: menos de 100 mensagens por segundo.
- Não há necessidade de reter eventos nem de reprocessá-los (replay).

## Decisão

Adotar o **RabbitMQ** como broker de mensagens entre os serviços.

## Justificativa

- **Experiência operacional:** a equipe já opera RabbitMQ, o que reduz risco e curva de aprendizado.
- **Volume:** com menos de 100 msg/s, o RabbitMQ atende com folga. A escala do Kafka não traz benefício aqui.
- **Sem retenção:** sem requisito de retenção de eventos, o log persistente do Kafka seria complexidade sem retorno.

## Consequências

**Positivas**

- Operação mais simples, com tecnologia já dominada pela equipe.
- Menos infraestrutura e menor custo de manutenção do que um cluster Kafka.

**Negativas / trade-offs aceitos**

- **Não há replay de eventos.** Mensagens consumidas e confirmadas (ack) são removidas da fila e não podem ser relidas.
- Se o volume crescer muito acima do previsto, pode ser preciso reavaliar.

## Reavaliação

Se surgir a necessidade de replay ou retenção de eventos, isso será tratado como **uma nova decisão** (novo ADR), que poderá substituir este.
