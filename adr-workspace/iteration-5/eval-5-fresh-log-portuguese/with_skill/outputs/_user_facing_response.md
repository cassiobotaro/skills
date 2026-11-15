Pronto. Documentei a decisão. Como o repositório ainda não tinha nenhum ADR, inicializei um log de decisões novo em `doc/adr/` (no formato Michael Nygard / adr-tools): criei o ADR semente padrão e, em seguida, a sua decisão como ADR 0002.

A conversa está em português, então a prosa (título e corpo) está em português; mas o "andaime" que as ferramentas leem (o rótulo `Date:`, os cabeçalhos `## Status`/`## Context`/`## Decision`/`## Consequences` e a palavra de status `Accepted`) fica em inglês canônico — é o que mantém os arquivos importáveis pelo Structurizr e pelo `adr generate` sem que a data ou o status virem padrão silenciosamente.

Arquivos criados:

1. `doc/adr/0001-registrar-decisoes-de-arquitetura.md`

```markdown
# 1. Registrar decisões de arquitetura

Date: 2026-06-07

## Status

Accepted

## Context

Precisamos registrar as decisões de arquitetura tomadas neste projeto.

## Decision

Vamos usar Architecture Decision Records, conforme [descrito por Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).

## Consequences

Veja o artigo de Michael Nygard, indicado acima. Para um conjunto de ferramentas leve de ADRs, veja o [adr-tools](https://github.com/npryce/adr-tools) de Nat Pryce.
```

2. `doc/adr/0002-adotar-rabbitmq-em-vez-de-kafka-para-a-fila-de-mensagens.md`

```markdown
# 2. Adotar RabbitMQ em vez de Kafka para a fila de mensagens

Date: 2026-06-07

## Status

Accepted

## Context

Os serviços precisam de uma fila de mensagens para se comunicar entre si. O volume de tráfego é baixo, abaixo de 100 mensagens por segundo, e não há necessidade de reter os eventos para reprocessamento posterior. A equipe já possui experiência operacional com RabbitMQ. As principais opções consideradas foram RabbitMQ e Kafka.

## Decision

Vamos adotar o RabbitMQ como fila de mensagens entre os serviços, em vez do Kafka.

## Consequences

A operação fica mais simples por se apoiar na experiência que a equipe já tem com RabbitMQ, sem o custo de aprender e operar o Kafka.

Abrimos mão do replay de eventos, já que o RabbitMQ não retém os eventos da forma que o Kafka faz. Se um dia precisarmos de retenção e reprocessamento de eventos, isso será objeto de uma nova decisão.
```

Observações: registrei só o que você descreveu — nenhuma força, alternativa ou consequência inventada. O trade-off que vocês aceitaram (abrir mão do replay de eventos) está em Consequences, e a porta para uma decisão futura está explícita. Status `Accepted` porque você apresentou como decisão já tomada; se ainda estiver em aberto na equipe, é só avisar que troco para `Proposed`.
