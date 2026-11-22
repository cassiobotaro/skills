Registrei a decisão como ADR 2, com status `Accepted`. O repositório não tinha log de decisões, então criei `doc/adr/` e um ADR de abertura.

- **`doc/adr/0002-adotar-rabbitmq-em-vez-de-kafka-para-a-fila-de-mensagens.md`**: a decisão em si. O contexto traz os motivos que você deu: experiência operacional da equipe com RabbitMQ, volume abaixo de 100 mensagens por segundo e nenhuma necessidade de retenção de eventos. A decisão é "Vamos adotar o RabbitMQ, em vez do Kafka, como fila de mensagens entre os serviços". As consequências registram que abrimos mão do replay de eventos e que, se um dia precisarmos dele, será uma nova decisão.
- **`doc/adr/0001-registrar-decis-es-de-arquitetura.md`**: o ADR 1, que registra a própria adoção de ADRs. Ele nasce junto com qualquer log novo, seguindo o padrão do `adr init`. Traduzi o texto para português, para o log ficar no mesmo idioma.

O texto está em português, como a conversa. Mantive em inglês `Date:`, os títulos `## Status`, `## Context`, `## Decision` e `## Consequences`, e a palavra `Accepted`, porque o adr-tools e outras ferramentas leem esses termos exatos. O acento some só do nome do arquivo (`decis-es`), não do título.

Não escrevi nenhum benefício além dos que você citou. Se houver alternativas que a equipe pesou ou riscos que você aceitou, me diga e eu acrescento ao ADR 2.
