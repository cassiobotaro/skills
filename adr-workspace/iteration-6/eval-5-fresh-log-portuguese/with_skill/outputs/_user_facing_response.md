Como o projeto ainda não tinha um log de decisões, criei um do zero em `doc/adr/` (o diretório padrão do adr-tools), com dois arquivos:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` — o ADR semente, que registra a própria decisão de manter um log de ADRs no formato Michael Nygard. É o equivalente ao que o `adr init` cria.
- `doc/adr/0002-adotar-rabbitmq-em-vez-de-kafka-para-a-fila-de-mensagens.md` — a sua decisão.

O ADR 2 ficou assim:

```markdown
# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Date: 2026-07-21

## Status

Accepted

## Context

Os serviços precisam trocar mensagens entre si por meio de uma fila. As duas opções consideradas foram RabbitMQ e Kafka.

O volume de mensagens é baixo: menos de 100 mensagens por segundo. Não há necessidade de retenção de eventos.

A equipe já tem experiência operacional com RabbitMQ.

## Decision

Vamos adotar o RabbitMQ como fila de mensagens entre os serviços.

## Consequences

A operação se apoia na experiência que a equipe já tem com RabbitMQ.

Abrimos mão do replay de eventos, que o Kafka ofereceria pela retenção do log. Se um dia precisarmos dessa capacidade, ela será objeto de uma nova decisão.
```

Uma observação sobre o idioma: o texto está em português, mas o rótulo `Date:`, os quatro títulos `## Status` / `## Context` / `## Decision` / `## Consequences` e a palavra de status (`Accepted`) ficam em inglês de propósito. O adr-tools não tem localização e as ferramentas que leem esses arquivos procuram exatamente esses literais — traduzi-los faria a data e o status serem silenciosamente ignorados.
