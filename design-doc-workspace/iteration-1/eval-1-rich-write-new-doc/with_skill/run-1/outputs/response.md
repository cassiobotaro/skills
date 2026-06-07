Pronto! Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`.

Você me deu os cinco pontos que um design doc honesto precisa — problema, fronteiras,
solução, alternativas e o impacto em outros times —, então escrevi direto em vez de
ficar te questionando. Em português, seguindo a língua da nossa conversa.

O que o doc cobre:

- **Visão geral, escopo e contexto** — geração síncrona estourando o timeout de 30s,
  ~12% de falhas acima de 50 mil linhas e os tickets semanais de suporte. RabbitMQ e S3
  como infra que já temos.
- **Objetivos e fora de escopo** — zerar o timeout (tirando a geração do ciclo da
  request) e suportar 100 mil linhas via streaming. Fora de escopo: o download imediato,
  que deixa de existir.
- **A solução** — diagrama de containers (estilo C4) e diagrama de sequência do fluxo
  (API enfileira → worker gera em streaming → sobe ao S3 → e-mail com link assinado),
  cada um seguido de texto, mais os fragmentos de API que mudam e a nota de dados/PII.
- **Trade-offs** — com destaque para o custo central que vocês aceitaram: **o usuário
  perde o download imediato** das exportações pequenas em troca de um caminho único.
- **Alternativas** — síncrono com timeout maior e BI externo (ambas descartadas, com o
  motivo), mais "não fazer nada".
- **Concerns transversais** — Segurança (link assinado com PII) e Plataforma (fila
  compartilhada) como times impactados, sugeridos como revisores; mais a quebra de
  compatibilidade do contrato da API.
- **Testabilidade/observabilidade**, **plano de implantação** e **perguntas em aberto**.

Duas notas:

1. Os diagramas estão como blocos ```mermaid``` inline (renderizam no GitHub/GitLab). O
   servidor MCP de validação do Mermaid estava fora do ar agora, então não consegui
   validar pela ferramenta — a sintaxe é padrão, mas vale conferir o render quando puder.

2. Deixei como **perguntas em aberto** (e marcado `_(a preencher)_` no header) o que eu
   não tinha como inventar sem você. Quando puder, me confirma:
   - **Autores e revisores nomeados** (quem assina; quem de Plataforma e Segurança revisa).
   - **TTL do link assinado** e **política de retenção/expiração** dos arquivos no S3.
   - **Fila dedicada vs. compartilhada** e **limite de concorrência** do worker.
   - **O que acontece quando a exportação falha** (retry automático? aviso ao usuário?
     reprocessamento via suporte?).
   - Se haverá **demanda real acima de 100 mil linhas** — está fora do escopo desta
     entrega, mas afeta o desenho se for aparecer logo.

É só me passar essas respostas que eu incorporo no corpo do doc e atualizo o header.
