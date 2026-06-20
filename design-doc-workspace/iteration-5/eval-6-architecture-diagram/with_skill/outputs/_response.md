Escrevi o design doc do serviço de entrega de webhooks em `docs/design/servico-de-webhooks.md`.

Como você já trouxe o problema, a solução, o trade-off, as alternativas (incluindo o "não fazer nada") e os times impactados, escrevi direto, sem entrevista. O documento ficou organizado assim:

- **Cabeçalho** (estado: Rascunho; revisores de SRE e Segurança a nomear) e **glossário** (webhook, HMAC, backoff, DLQ, AMQP, PII, SRE, SLA/SLO).
- **Visão geral** e **escopo/contexto** com o problema atual (POST direto, sem retry, sem visibilidade, eventos perdidos em produção).
- **Objetivos** (mensuráveis, com o mecanismo) e **fora de escopo** (entrega ao-menos-uma-vez, sem fan-out, sem UI por enquanto).
- **A solução** com:
  - **Diagrama de arquitetura (C4 container)** seguido de prose explicando cada componente;
  - **Diagrama de sequência** do fluxo de entrega, com o caminho de falha (retry/backoff → DLQ);
  - fragmentos de **API/payload** (assinatura HMAC, consulta e reenvio) e **dados/sensibilidade** (segredo HMAC por cliente, PII no payload).
- **Trade-offs** explícitos (com o custo aceito: entrega assíncrona, atraso de alguns segundos, ao-menos-uma-vez, mais peças para operar).
- **Alternativas** numa tabela com marcadores textuais (lógica de retry por serviço, SaaS tipo Svix, não fazer nada).
- **Preocupações transversais** (Segurança, Infra/SRE, Compatibilidade), **testabilidade/observabilidade**, **plano de implantação** com rollback e **questões em aberto**.

Sobre o diagrama: as ferramentas de validação/exportação do Structurizr e o renderizador de Mermaid não estavam disponíveis neste ambiente (permissões negadas e nenhum CLI instalado), então **não consegui gerar um arquivo de imagem**. Seguindo o caminho de degradação graciosa da skill, embuti o diagrama de arquitetura como um bloco ```mermaid``` que renderiza nativamente no GitHub/GitLab, com a fonte em **Structurizr DSL** dobrada num `<details>` logo abaixo para quem for editar o modelo. A fonte Mermaid também ficou salva em `docs/design/diagrams/arquitetura.mmd` caso você queira renderizá-la para imagem depois (ex.: `mmdc -i arquitetura.mmd -o arquitetura.svg`).

Pontos que valem a sua atenção, marcados como questões em aberto no doc: retenção do histórico/payloads e armazenamento+rotação dos segredos HMAC (com Segurança), parâmetros do backoff e ownership operacional (com SRE), e o SLA de atraso aceitável agora que a entrega é assíncrona.
