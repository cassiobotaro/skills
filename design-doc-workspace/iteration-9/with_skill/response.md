Escrevi o design doc em `docs/design/exportacao-de-relatorios-em-background.md`.

Seu prompt já trazia o essencial — o problema com número (12% de falha acima de 50 mil
linhas), os objetivos (zerar timeouts, aguentar 100 mil linhas), a solução, as duas
alternativas descartadas com o motivo, o custo aceito (fim do download imediato) e os
times impactados —, então escrevi direto em vez de te entrevistar.

**Estrutura do documento**

Header · Glossário · Visão geral · Escopo e contexto · Objetivos e fora de escopo · A
solução (visão geral, arquitetura, fluxo, dados e sensibilidade) · Trade-offs ·
Alternativas consideradas · Preocupações transversais · Testabilidade e observabilidade ·
Questões em aberto.

**Diagramas**

- **Arquitetura (C4, nível de containers)** — escrita em Structurizr DSL, validada com
  `structurizr/structurizr validate` e renderizada para
  `docs/design/diagrams/arquitetura.svg` (export PlantUML → SVG). O documento traz a
  imagem e a DSL dobrada num bloco `<details>`, que é a fonte da verdade do modelo.
- **Fluxo da exportação** — diagrama de sequência em Mermaid, que o GitHub/GitLab
  renderizam direto. Não havia Mermaid MCP nem `mmdc` disponíveis aqui, então o bloco
  não foi renderizado nesta máquina; cole em <https://mermaid.live> se quiser conferir.

**Onde não inventei nada e preciso de você**

Ficaram em *Questões em aberto* os pontos que o prompt não estabelecia, principalmente:

1. **Autores e revisores** — o header está com `(a preencher)`. Sugeri as áreas
   (Plataforma pela fila compartilhada, Segurança pelo link com PII); faltam os nomes.
2. **Caminho de erro** — o diagrama de sequência mostra só o caminho feliz. Quantas
   tentativas um job falho recebe, o que o usuário vê quando falha e se existe fila de
   mensagens mortas não estavam definidos, e eu não ia inventar.
3. **Validade do link e retenção no S3** — o arquivo com PII passa a ficar armazenado e
   o link viaja por e-mail; os prazos são decisão de Segurança.
4. **Isolamento da fila** no RabbitMQ compartilhado, a fechar com Plataforma.
5. **Acompanhamento da exportação em andamento** — com o fim da resposta imediata, o
   usuário fica sem sinal até o e-mail chegar; não ficou claro se haverá tela de status.
6. **Tecnologias do worker** (linguagem, biblioteca de planilha) — por isso os containers
   do diagrama saem sem tecnologia declarada, exceto a fila (RabbitMQ).

Se você responder 1 a 3, eu já incorporo no documento — são os que mais mudam o desenho.
