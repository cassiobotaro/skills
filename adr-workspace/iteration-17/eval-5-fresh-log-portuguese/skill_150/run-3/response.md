Registrei a decisão como ADR 0002. O repositório não tinha log de decisões, então criei `doc/adr/` com um ADR inicial, como o `adr init` faz.

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md` é o ADR inicial, traduzido para português, que registra o uso de ADRs.
- `doc/adr/0002-adotar-rabbitmq-em-vez-de-kafka-para-a-fila-de-mensagens.md` é a sua decisão, com status `Accepted` e data 2026-11-22.

O ADR 0002 usa só o que você informou:
- **Contexto:** a equipe tem experiência operacional com RabbitMQ, o volume é menor que 100 mensagens por segundo e não há necessidade de retenção de eventos.
- **Decisão:** adotar o RabbitMQ, e não o Kafka, como fila entre os serviços.
- **Consequências:** abrimos mão do replay de eventos, e precisar dele no futuro será uma nova decisão. A operação segue apoiada na experiência da equipe.

Os títulos e os textos das seções estão em português. Os rótulos que o adr-tools e o Structurizr leem (`Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences` e `Accepted`) ficaram em inglês de propósito, para que as ferramentas continuem lendo os arquivos.

Não fiz commit.
