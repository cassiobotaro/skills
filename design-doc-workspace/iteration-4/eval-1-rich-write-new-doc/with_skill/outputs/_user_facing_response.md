Pronto! Criei o design doc em `docs/design/async-report-export-service.md`.

Como o seu pedido já trazia tudo que um design doc honesto precisa — o problema (12% de falha por timeout acima de 50 mil linhas, ticket semanal de suporte), os limites (zerar timeouts, aguentar 100 mil linhas), a solução (API enfileira → worker gera em streaming → S3 → link assinado por e-mail), as alternativas (timeout maior e BI externo, ambas descartadas, mais "não fazer nada") e o blast radius (Plataforma na fila compartilhada, Segurança no link com PII) — eu fui direto para a escrita, sem te interrogar. O repositório estava vazio e sem template, então usei a estrutura padrão escolhendo só as seções que esse problema pede.

O que ele tem:

- **Cabeçalho** em estado Rascunho, datado de hoje (2026-06-07), com revisores sugeridos: Plataforma e Segurança.
- **Glossário** logo no início (API, RabbitMQ, AMQP, S3, link assinado, PII, CSV/XLSX, BI, TTL, DLQ, vhost).
- **Visão geral / Escopo e contexto / Objetivos e fora de escopo** — incluindo o "fora de escopo" do download imediato, que deixa de existir.
- **A solução** com diagrama de containers (C4) e diagrama de sequência do fluxo, cada um seguido de texto explicando os componentes e as interações, mais o fragmento relevante de API (`200` com arquivo → `202` com `jobId`) e a sensibilidade dos dados (PII).
- **Trade-offs** com o custo aceito dito sem rodeio: o usuário perde o download imediato, e até a exportação pequena vira assíncrona — em troca de um caminho único e do fim dos timeouts.
- **Alternativas** numa tabela (a escolhida marcada, as duas descartadas com o porquê, e "não fazer nada").
- **Cross-cutting concerns** separados para Segurança (TTL, criptografia, retenção, auditoria) e Plataforma (isolamento da fila, concorrência, retry/DLQ), além de compatibilidade.
- **Testabilidade/observabilidade**, **plano de implantação** por fases com rollback, e **questões em aberto**.

Dois detalhes:

- Deixei os **autores como `_(a preencher)_`** — me diga os nomes (e se quiser nomear pessoas específicas dos times de Plataforma e Segurança como revisores) que eu completo.
- Os dois diagramas Mermaid renderizam direto no GitHub/GitLab, mas **não consegui validá-los por ferramenta automática nesta sessão** (o servidor de validação estava indisponível); mantive a sintaxe conservadora. Se você rodar um preview e algo destoar, me avise que eu ajusto.

Quer que eu preencha os autores/revisores ou detalhe mais alguma das questões em aberto (idempotência, TTL do link, transição do contrato da API)?
