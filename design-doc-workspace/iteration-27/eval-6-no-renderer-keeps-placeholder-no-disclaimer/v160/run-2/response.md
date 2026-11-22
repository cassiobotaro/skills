Escrevi o design doc em `docs/design/webhooks-de-saida.md`, em português, com o estado "Rascunho". Não validei o DSL nem renderizei a imagem, porque não há Docker nem CLI do Structurizr aqui.

**O que o doc tem**
- **Cabeçalho, glossário, visão geral e contexto:** o glossário cobre evento de domínio, tentativa, HMAC, backoff exponencial e DLQ.
- **Objetivos:** nenhum evento perdido por indisponibilidade do cliente, e registro de cada tentativa.
- **Arquitetura:** diagrama de containers em Structurizr DSL, dobrado em `<details>`, com texto explicando os componentes.
- **Fluxo de entrega com retry:** diagrama de sequência em Mermaid, que renderiza direto no Markdown, também com texto explicativo.
- **Trade-offs:** o custo central é a entrega não imediata em alguns casos. Também registrei o serviço novo para operar.
- **Alternativas:** não fazer nada, o SaaS (custo por evento e payload fora da borda) e o serviço próprio, que foi o escolhido.

**Pendências**
- **Imagem da arquitetura:** a referência `diagrams/arquitetura.svg` é um placeholder, e o arquivo ainda não existe. É preciso renderizar o DSL na passagem manual.
- **Tecnologias:** deixei sem tecnologia o que você não informou, como a DLQ e o serviço de entrega.
- **Autores e revisores:** estão como "A confirmar". Sugeri segurança e os times dos serviços que hoje fazem o POST.
- **Questões em aberto:** listei 12 pontos que você não tinha definido, entre eles:
  - o que conta como entrega bem-sucedida;
  - os intervalos do backoff;
  - como agendar a próxima tentativa;
  - o destino dos eventos na DLQ;
  - o segredo do HMAC;
  - entregas repetidas;
  - a ordem dos eventos;
  - a migração dos serviços atuais;
  - métricas e alertas;
  - o que fica fora de escopo;
  - a retenção do histórico no Postgres.

Passei o unslop no texto. As edições foram pequenas: tirei voz passiva e duas afirmações que ninguém tinha dito, como quem consulta o log e que "o processo da DLQ ainda não existe".

Se você me passar as respostas dessas questões, eu as incorporo ao corpo do doc.
