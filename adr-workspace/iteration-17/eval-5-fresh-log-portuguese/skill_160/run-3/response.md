Registrei a decisão como ADR 2, com status `Accepted`. O repositório não tinha log de decisões, então criei `doc/adr/` com um ADR 1 de abertura.

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md`: é o ADR inicial que o `adr init` costuma gerar, traduzido para português. Ele só registra que o projeto passa a usar ADRs.
- `doc/adr/0002-adotar-rabbitmq-em-vez-de-kafka-para-a-fila-de-mensagens.md`: é a sua decisão.
  - **Contexto:** a equipe tem experiência operacional com RabbitMQ, o volume é menor que 100 mensagens por segundo e não há necessidade de retenção de eventos.
  - **Decisão:** "Vamos adotar o RabbitMQ, em vez do Kafka, como fila de mensagens entre os serviços."
  - **Consequências:** abrimos mão do replay de eventos, e se um dia precisarmos dele será uma nova decisão. Em troca, a operação se apoia na experiência que a equipe já tem.

O texto está em português, mas `Date:`, os títulos `## Status`, `## Context`, `## Decision` e `## Consequences` e a palavra `Accepted` ficam em inglês. É o formato que o adr-tools e o importador `!adrs` do Structurizr leem. No nome do arquivo, as letras acentuadas viram hífen (`decis-es`), como o adr-tools faz.

Usei apenas o que você informou, sem acrescentar motivos nem alternativas.
