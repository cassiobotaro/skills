Pronto! Escrevi o design doc do serviço de entrega de webhooks em `docs/design/servico-de-webhooks.md`.

O documento cobre, em português:

- **Visão geral, escopo e contexto** — o problema atual (POST direto inline, sem retry nem visibilidade, perdendo eventos em produção).
- **Objetivos e fora de escopo** — eliminar perda de eventos, centralizar a entrega, dar visibilidade e garantir autenticidade; deixando ordenação, exactly-once, autosserviço e outros transportes de fora.
- **A solução** com **diagrama de arquitetura (contêineres C4 em Mermaid)** e um **diagrama de sequência** do fluxo de entrega (caminho feliz, retry com backoff e DLQ), cada um seguido de texto explicando os componentes; mais dados/sensibilidade e fragmentos de API/payload.
- **Trade-offs explícitos** — o custo aceito (entrega assíncrona, latência de alguns segundos, at-least-once) em troca de retry, durabilidade e visibilidade.
- **Alternativas consideradas** em tabela, incluindo "não fazer nada", retry por serviço e SaaS (Svix).
- **Cross-cutting concerns** para SRE (nova fila/serviço) e Segurança (HMAC e segredos por cliente), ambos sugeridos como revisores no cabeçalho.
- **Testabilidade/observabilidade, plano de implantação incremental e perguntas em aberto.**

Há também um **glossário** no início (HMAC, AMQP, DLQ, etc.).

Sobre o **diagrama em imagem**: não consegui renderizar um arquivo de imagem nesta sessão — os servidores de validação/render do Structurizr e do Mermaid, e o render local, não estavam disponíveis. Segui o caminho de degradação graciosa da skill: os diagramas estão embutidos como blocos ```mermaid``` (renderizam direto no GitHub/GitLab) e a fonte do diagrama de arquitetura também ficou versionada em `docs/design/diagrams/arquitetura-webhooks.mmd`. Deixei uma nota no doc de que o diagrama não foi validado por ferramenta automática.

Como é um rascunho, vale revisar comigo as perguntas em aberto (provisionamento de assinaturas, armazenamento dos segredos, retenção do histórico/PII, tratamento da DLQ e os limites de retry/backoff).
