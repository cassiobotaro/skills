# ADR 0001: Adotar RabbitMQ em vez de Kafka para a fila de mensagens entre serviços

- **Status:** Aceita
- **Data:** 2026-11-22

## Contexto

Os serviços precisam de uma fila de mensagens para se comunicarem. As opções consideradas foram RabbitMQ e Kafka.

Fatores relevantes:

- A equipe já tem experiência operacional com RabbitMQ.
- O volume é baixo: menos de 100 mensagens por segundo.
- Não há necessidade de retenção de eventos.

## Decisão

Adotamos o **RabbitMQ** como broker de mensagens entre os serviços.

## Justificativa

- **Experiência operacional:** a equipe já opera RabbitMQ, o que reduz risco e curva de aprendizado.
- **Volume baixo:** com menos de 100 msg/s, a capacidade de alto throughput do Kafka não traz benefício e o custo operacional dele não se justifica.
- **Sem retenção de eventos:** o principal diferencial do Kafka (log persistente com replay) não é um requisito.

## Consequências

### Positivas

- Operação mais simples e familiar para a equipe.
- Menor complexidade de infraestrutura.

### Negativas / trade-offs aceitos

- **Sem replay de eventos:** mensagens consumidas e confirmadas deixam de estar disponíveis. Aceitamos abrir mão dessa capacidade.

## Revisão

Se no futuro houver necessidade de replay ou retenção de eventos, ou se o volume crescer de forma significativa, isso será tratado como uma **nova decisão** (novo ADR), que poderá substituir esta.

## Alternativas consideradas

- **Kafka:** rejeitado, pelos motivos acima (sem experiência operacional da equipe, volume baixo e sem necessidade de retenção/replay).
