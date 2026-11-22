# ADR 0001: Adotar RabbitMQ em vez de Kafka para a fila de mensagens entre serviços

- **Status:** Aceita
- **Data:** 2026-11-22

## Contexto

Os serviços precisam se comunicar de forma assíncrona por meio de uma fila de mensagens. As opções consideradas foram RabbitMQ e Kafka. Fatores relevantes:

- A equipe já tem experiência operacional com RabbitMQ.
- O volume é baixo: menos de 100 mensagens por segundo.
- Não há necessidade de retenção de eventos.

## Decisão

Adotaremos o **RabbitMQ** como broker de mensagens entre os serviços.

## Justificativa

- **Experiência operacional:** a equipe já opera RabbitMQ, o que reduz risco, curva de aprendizado e custo de operação.
- **Volume baixo:** menos de 100 msg/s está bem dentro da capacidade do RabbitMQ. A escala e o throughput do Kafka não trazem benefício aqui.
- **Sem retenção:** como não precisamos guardar eventos, o log persistente do Kafka não é necessário.

## Consequências

### Positivas

- Operação mais simples e familiar para a equipe.
- Menor complexidade de infraestrutura.

### Negativas / trade-offs aceitos

- **Sem replay de eventos.** As mensagens são removidas da fila depois de consumidas, e não será possível reprocessar o histórico.
- Se o volume crescer muito acima do previsto, o RabbitMQ pode deixar de ser adequado.

## Revisão

Se um dia precisarmos de replay ou retenção de eventos, isso será tratado como **uma nova decisão** (novo ADR), e não como um ajuste a este.
