Como ainda não havia um log de decisões no projeto, inicializei um novo (equivalente ao `adr init`) em `doc/adr/` e registrei a sua decisão. Criei dois arquivos:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` — o ADR semente, que registra a própria decisão de adotar ADRs no projeto.
- `doc/adr/0002-adotar-rabbitmq-em-vez-de-kafka-para-a-fila-de-mensagens.md` — a sua decisão.

O ADR 0002 documenta, no formato Michael Nygard (em português, para acompanhar a língua do log):

- **Contexto**: a necessidade de troca assíncrona de mensagens entre os serviços, as duas tecnologias avaliadas (RabbitMQ e Kafka), a experiência operacional da equipe com RabbitMQ, o volume baixo (abaixo de 100 mensagens/segundo) e a ausência de necessidade de retenção de eventos.
- **Decisão**: adotar o RabbitMQ em vez do Kafka como fila de mensagens entre os serviços.
- **Consequências**: o aproveitamento da experiência existente, a adequação ao volume atual sem necessidade da retenção do Kafka e, como contrapartida aceita, abrir mão do replay de eventos — que, se for necessário no futuro, será objeto de uma nova decisão.

Os arquivos seguem as convenções do adr-tools (numeração sequencial, nomes `NNNN-slug.md`). Mantive apenas o que você descreveu, sem inventar forças, alternativas ou consequências adicionais.
