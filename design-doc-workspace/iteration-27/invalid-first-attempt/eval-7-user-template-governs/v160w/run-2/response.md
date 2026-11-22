Escrevi o documento em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`, seguindo o `TEMPLATE.md` sem acrescentar nem tirar seções.

- **Alternativas e trade-off:** o template não tem seção de alternativas. Coloquei as duas descartadas e os +5ms como subseções dentro de **Proposta**, para não mudar a estrutura.
- **Cabeçalho:** o número é DD-2026-001, porque não havia outro documento em `docs/design/`. Estado é Rascunho, o autor é você e as datas são 2026-11-22. Deixei **Revisores** em branco.
- **O que é meu, não seu:**
  - O fluxo com gravação atômica (`SET NX` com expiração).
  - Os riscos, como Redis fora do ar, a janela de 24h e a chave mal definida.
  - As três fases do rollout (sombra, descarte parcial, descarte total).

  Marquei o rollout como proposta do autor. Revise esses pontos antes de mandar para a arquitetura.
- **Números:** usei só os seus: 4%, meta abaixo de 0,1%, +5ms, 24h e duas reclamações. Os critérios de avanço do rollout ficaram qualitativos, porque você não deu limites.
- **Perguntas abertas (7):**
  - Se o Redis cair, o serviço deixa passar (fail-open) ou bloqueia a ingestão (fail-closed)?
  - Quem gera a chave idempotente e quais campos a compõem?
  - Os +5ms valem para a média ou para o p99?
  - Qual o volume de eventos e o tamanho do Redis para 24h de chaves?
  - Existem reenvios depois de 24h?
  - Quais são os critérios numéricos de avanço entre as fases do rollout?
  - Quem são os revisores?

Não commitei nada.
