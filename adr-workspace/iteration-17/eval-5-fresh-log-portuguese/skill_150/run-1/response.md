Documentei a decisão como ADR 2, com status `Accepted`. Não rodei nenhuma ferramenta nem validação sobre os arquivos.

O repositório não tinha log de decisões, então criei `doc/adr/` e um ADR 0001 de abertura, como o `adr init` faz. Ele registra o uso de ADRs, traduzido para português. Os dois arquivos estão datados de 2026-11-22:

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md`
- `doc/adr/0002-adotar-rabbitmq-em-vez-de-kafka-para-a-fila-de-mensagens.md`

O texto do ADR 2 usa só o que você informou:
- **Contexto:** os serviços precisam de uma fila de mensagens, a equipe tem experiência operacional com RabbitMQ, o volume é de menos de 100 mensagens por segundo e não há necessidade de retenção de eventos.
- **Decisão:** vamos adotar o RabbitMQ, e não o Kafka, como fila de mensagens entre os serviços.
- **Consequências:** abrimos mão do replay de eventos, e se um dia precisarmos dele será uma nova decisão. A operação se apoia na experiência que a equipe já tem.

O texto está em português, mas os rótulos (`Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences`) e o status `Accepted` ficam em inglês. É o formato que o adr-tools e o importador `!adrs` do Structurizr leem. Por isso os nomes dos arquivos também perdem os acentos (`decis-es`).
