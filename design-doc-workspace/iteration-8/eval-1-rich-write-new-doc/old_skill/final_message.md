Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`. Como você já trouxe o essencial — problema com números (timeout de 30s no gateway, ~12% de falha acima de 50 mil linhas, ticket semanal), solução, alternativas descartadas, o trade-off aceito e os times impactados — escrevi direto, sem te interrogar de novo.

O que o documento cobre:

- **Cabeçalho e glossário** — estado "Rascunho", data de hoje; o glossário define os termos que o doc usa (PII, link assinado, BI, streaming etc.).
- **Contexto, objetivos e fora de escopo** — objetivos mensuráveis (zerar falhas por timeout; suportar 100 mil linhas) e a exclusão explícita que alguém poderia esperar: não haverá caminho síncrono nem para exportações pequenas.
- **Design** — visão da solução, arquitetura C4 (contêineres), o fluxo de exportação em diagrama de sequência Mermaid e uma seção de dados e sensibilidade (PII no S3 atrás de link assinado).
- **Trade-offs explícitos** — incluindo os custos: perda do download imediato, carga nova no RabbitMQ compartilhado e nova superfície de exposição de PII.
- **Alternativas consideradas** — "não fazer nada", timeout maior (só empurra o problema), BI externa (custo + dado de cliente), e por que a escolhida venceu.
- **Preocupações transversais** — uma subseção para Plataforma (fila compartilhada) e outra para Segurança (link assinado com PII), os dois sugeridos como revisores no cabeçalho.

Sobre os diagramas:

- A arquitetura está como **Structurizr DSL**, validada com `structurizr/structurizr` via Docker (sem erros). Não há renderizador de imagem neste ambiente, então a referência `diagrams/exportacao-relatorios-containers.svg` ficou como placeholder com uma nota para renderizar na passada manual — o DSL dobrado no `<details>` é a fonte.
- O diagrama de sequência é um bloco ` ```mermaid ` que o GitHub/GitLab renderizam nativamente. Não consegui validá-lo aqui (sem MCP do Mermaid nem mermaid-cli local); se quiser conferir antes do commit, cole em https://mermaid.live.

Ficaram na seção **Questões em aberto** os pontos que só vocês podem responder — vale preencher antes de circular o doc:

1. Quem assina como autor e quem revisa por Plataforma e Segurança?
2. O que acontece quando um job falha (retentativa, destino da mensagem, aviso ao usuário)? O fluxo documentado é só o caminho feliz.
3. Validade do link assinado e retenção dos arquivos no S3?
4. O e-mail sai do próprio worker ou de um serviço de notificação existente?
5. O worker lê do banco primário ou de uma réplica?

Duas sugestões de seções que fariam bem ao doc quando essas respostas existirem (não inventei conteúdo para elas): **Testabilidade e observabilidade** — os objetivos já dão as métricas (taxa de falha por timeout, exportação de 100 mil linhas) — e um **Plano de implantação**, já que a migração muda o comportamento das exportações pequenas que hoje funcionam.
