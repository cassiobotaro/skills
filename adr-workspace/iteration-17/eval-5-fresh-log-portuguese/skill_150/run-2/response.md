Registrei a decisão como ADR 2 em `doc/adr/`, com status `Accepted` e data 2026-11-22.

O projeto não tinha nenhum log de decisões. Por isso criei também o ADR 1, que é o registro padrão "Registrar decisões de arquitetura" (equivalente ao `adr init`). Escrevi os dois em português. Os rótulos e cabeçalhos ficam em inglês (`Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences`, `Accepted`), porque o adr-tools e o importador `!adrs` do Structurizr leem esses termos exatos.

Arquivos criados:
- `doc/adr/0001-registrar-decis-es-de-arquitetura.md`
- `doc/adr/0002-adotar-rabbitmq-em-vez-de-kafka-para-a-fila-de-mensagens.md`

O ADR 2 usa só o que você informou:
- **Contexto:** a equipe tem experiência operacional com RabbitMQ, o volume é menor que 100 mensagens por segundo e não há necessidade de retenção de eventos.
- **Decisão:** adotar o RabbitMQ em vez do Kafka como fila entre os serviços.
- **Consequências:** abrimos mão do replay de eventos, e precisar dele no futuro será uma nova decisão. A operação se apoia na experiência que a equipe já tem.

Não inventei motivos nem alternativas além do que você disse. Se quiser acrescentar outro custo aceito ou outra alternativa considerada, me diga. Depois que o ADR é aceito, o corpo não se edita. Uma mudança futura vira um novo ADR que o substitui.
