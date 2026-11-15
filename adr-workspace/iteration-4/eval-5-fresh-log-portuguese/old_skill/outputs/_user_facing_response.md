Registrei a decisão. Como ainda não havia um log de decisões no projeto, iniciei um do zero em `doc/adr/` (equivalente a um `adr init`), em português, para que o registro fique consistente na língua em que vai ser mantido.

Arquivos criados:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` — ADR semente, que registra a própria decisão de usar ADRs no projeto (o ponto de partida de qualquer log).
- `doc/adr/0002-adotar-rabbitmq-para-a-fila-de-mensagens.md` — a sua decisão.

O ADR 0002 ficou assim:

- **Status:** Aceito.
- **Contexto:** os serviços precisam trocar mensagens por uma fila; as opções foram RabbitMQ e Kafka. A equipe já tem experiência operacional com RabbitMQ, o volume é baixo (abaixo de 100 msg/s) e não há necessidade de reter eventos. O Kafka ofereceria retenção e replay, recursos que não correspondem às necessidades atuais.
- **Decisão:** adotar o RabbitMQ como fila de mensagens entre os serviços.
- **Consequências:** a equipe opera com tecnologia que já conhece; o RabbitMQ atende ao volume atual sem a infraestrutura extra do Kafka; e abrimos mão da retenção e do replay de eventos — se isso for necessário no futuro, será uma nova decisão.

Os arquivos seguem o formato adr-tools (numeração sequencial, nomes `NNNN-slug.md`), então as suas ferramentas existentes funcionam neles sem alteração.

Uma observação: o `adr generate toc`/`graph` e o importador do Structurizr leem as palavras de status e os verbos de link em inglês. Como o log está em português, eles podem não acompanhar links traduzidos — só relevante se você for usar essas ferramentas específicas.
