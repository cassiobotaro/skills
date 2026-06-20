Escrevi o design doc do serviço central de entrega de webhooks e salvei em `docs/design/servico-de-webhooks.md`.

O documento cobre, em português:

- **Visão geral, escopo e contexto** — o problema atual (POST inline, sem retry, sem visibilidade, eventos perdidos em produção) com a infraestrutura existente (RabbitMQ, PostgreSQL).
- **Objetivos e fora de escopo** — não perder eventos (retry com backoff até 5 tentativas + DLQ), durabilidade, visibilidade, centralização e assinatura HMAC; exclusões explícitas (migração dos clientes, transformação de eventos, ordenação, UI).
- **A solução** — dispatcher e Admin API em Go, fila no RabbitMQ, histórico e assinaturas no Postgres, com o fluxo de entrega/retry e a assinatura HMAC detalhados.
- **Diagrama de arquitetura (C4 de containers)** — escrito como Structurizr DSL, dobrado num bloco `<details>` sob a referência da imagem, seguido de prosa explicando cada componente.
- **Trade-offs** — o custo aceito (entrega assíncrona, atraso de alguns segundos) em troca de retry, durabilidade e visibilidade, mais os custos de operação e a nova superfície de segurança.
- **Alternativas consideradas** — retry por serviço, SaaS tipo Svix e "não fazer nada", cada uma com seus trade-offs e o motivo da rejeição.
- **Aspectos transversais (Segurança e SRE)**, **testabilidade/observabilidade** e **questões em aberto**.

Sobre o diagrama: tentei validar e exportar o DSL pelo servidor MCP do Structurizr e procurar um renderizador local, mas o ambiente negou tanto o MCP quanto o acesso ao shell. Seguindo o caminho de degradação graciosa da skill, deixei a referência `diagrams/architecture.svg` como **placeholder** (com uma nota explícita no doc) e o DSL — que é a fonte de verdade da arquitetura — dobrado logo abaixo, pronto para gerar a imagem na passagem manual. A pasta `docs/design/diagrams/` já está criada para receber o SVG.
