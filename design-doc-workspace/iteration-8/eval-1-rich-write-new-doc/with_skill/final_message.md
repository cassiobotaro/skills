Criei o design doc em `docs/design/exportacao-relatorios-background.md`. Como você já trouxe o essencial — problema com números, solução, alternativas descartadas, o trade-off aceito e os times impactados — escrevi direto, sem te interrogar. O que ficou de fora do que você contou virou item nas **Questões em aberto**, não conteúdo inventado.

O que o documento cobre:

- **Cabeçalho e glossário** — estado Rascunho; revisores sugeridos dos times de Plataforma e Segurança (nomes a definir); glossário com PII, BI e link assinado.
- **Contexto e objetivos** — o fluxo síncrono atual, o timeout de 30s no gateway, os ~12% de falha acima de 50 mil linhas e os tickets semanais; metas mensuráveis: zerar os timeouts de exportação e suportar 100 mil linhas. Fora de escopo explícito: manter um caminho síncrono para exportações pequenas (a decisão do caminho único).
- **Design** — visão da solução, diagrama de containers C4 (fonte em Structurizr DSL dobrada num bloco `<details>`), diagrama de sequência Mermaid do fluxo de exportação, e uma seção de dados e sensibilidade (PII nos relatórios e no arquivo servido por link assinado).
- **Trade-offs explícitos** — incluindo os custos aceitos: perda do download imediato, carga na fila compartilhada e a nova superfície de segurança do link assinado.
- **Alternativas** — síncrono com timeout maior, BI externa e "não fazer nada", cada uma com o motivo do descarte.
- **Preocupações transversais** — uma subseção para Segurança e outra para Plataforma, com a sugestão de revisor de cada área.

Sobre os diagramas: o **DSL do C4 foi validado** com o Structurizr via Docker (sem erros), mas esta build da imagem não exporta PNG/SVG e não há PlantUML/Graphviz na máquina — então a referência de imagem (`diagrams/exportacao-relatorios-containers.svg`) ficou como placeholder, com uma nota para renderizar na revisão manual. Para gerar a imagem: `docker run --rm -it -p 8080:8080 -v "$PWD":/usr/local/structurizr structurizr/structurizr local` e exporte a view "Containers" pela UI em `http://localhost:8080`. O diagrama Mermaid **não foi validado aqui** (sem MCP nem mermaid-cli disponíveis), mas o GitHub/GitLab renderizam o bloco nativamente e você pode conferir em <https://mermaid.live>.

Ficaram 7 questões em aberto que só o time responde — as mais importantes: quem assina e revisa o doc, o comportamento em falha do worker (retentativas e o que o usuário vê), expiração do link assinado e retenção no S3, os limites da fila compartilhada com Plataforma, e como verificar em produção que a meta de zerar timeouts foi atingida. Quando tiver essas respostas, me chama que eu incorporo no documento.
