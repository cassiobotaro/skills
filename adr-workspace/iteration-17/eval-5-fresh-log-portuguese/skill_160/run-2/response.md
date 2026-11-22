Documentei a decisão como ADR 2, com status `Accepted` e data 2026-11-22. O repositório não tinha log de decisões, então criei `doc/adr/` e um ADR 1 de abertura.

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md` é o registro inicial do `adr init`, traduzido para português. Ele só diz que o projeto passa a usar ADRs.
- `doc/adr/0002-adotar-rabbitmq-em-vez-de-kafka-para-a-fila-de-mensagens.md` é a decisão em si:
  - **Contexto:** a equipe tem experiência operacional com RabbitMQ, o volume é baixo (menos de 100 mensagens/s) e não há necessidade de retenção de eventos.
  - **Decisão:** adotar o RabbitMQ, e não o Kafka, como fila entre os serviços.
  - **Consequências:** abrimos mão do replay de eventos, e precisar dele um dia será uma nova decisão. Em troca, a operação se apoia na experiência que a equipe já tem.

O texto é todo seu: não acrescentei motivos nem consequências além dos que você deu. Os títulos e o texto estão em português, mas `Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences` e `Accepted` ficam em inglês. Assim o `adr-tools` e o importador `!adrs` do Structurizr leem o arquivo sem problema. Os nomes dos arquivos perdem os acentos (`decis-es`) porque o slug só aceita letras e dígitos ASCII, mas os títulos dentro dos arquivos mantêm a acentuação.

Não fiz commit.
