Escrevi o design doc em `docs/design/servico-webhooks-saida.md`, em português, com o que você descreveu: problema, proposta, objetivos, trade-off aceito (entrega deixa de ser imediata em alguns casos), alternativas (não fazer nada e SaaS de webhooks) e dois diagramas.

- **Arquitetura**: um diagrama de containers em Structurizr DSL. A referência de imagem `diagrams/architecture.svg` é um placeholder e a imagem não foi gerada, porque aqui não há Docker nem CLI do Structurizr. O DSL está embutido no documento, dentro de um bloco `<details>`. Ele não foi validado, então rode `structurizr/structurizr validate` e exporte o SVG na passada manual.
- **Fluxo de entrega com retry**: um diagrama de sequência em Mermaid, direto no documento. Também não foi validado.
- **Tecnologias**: só usei as que você citou (Kafka, Postgres, HMAC). A DLQ e o serviço de entrega ficaram sem tecnologia, e as setas ficaram sem protocolo.

Perguntas para fechar o documento (também estão em "Questões em aberto"):
1. Quem são os autores e os revisores, e quais áreas devem revisar?
2. Qual é a meta mensurável (por exemplo, % de eventos entregues, tempo até a primeira tentativa) e o que fica fora de escopo?
3. Qual é o backoff concreto (intervalo inicial, fator, teto) e o que conta como falha (timeout, erro de conexão, resposta fora da faixa de sucesso)?
4. Qual é a tecnologia da DLQ e o que acontece com os eventos que chegam nela (alerta, reprocessamento, quem atua)?
5. Em que tecnologia o serviço de entrega será implementado, e de onde vem e como se gerencia o segredo HMAC de cada cliente?
6. O Kafka de eventos é da sua equipe ou de outra? Como será a migração dos serviços que hoje fazem o POST direto? Quem vai consumir a visibilidade das tentativas?
