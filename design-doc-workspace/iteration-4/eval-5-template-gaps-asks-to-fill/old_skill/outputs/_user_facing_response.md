Criei o rascunho seguindo o padrão dos docs em `docs/design/`, continuando a numeração (DD-2026-007 era o último):

`docs/design/dd-2026-008-busca-por-similaridade.md`

Preenchi **Resumo**, **Contexto** e **Proposta** com o que você me passou — o problema (busca por `LIKE`, ~30% sem resultado, o exemplo do "tênis de corrida amortecido" vs. "tênis running com amortecimento") e a proposta aprovada no refinamento (embeddings de título/descrição com modelo de similaridade de sentenças, armazenados no pgvector, busca vetorial com fallback pro `LIKE` quando o score vier baixo).

O padrão da casa também exige **Compensações**, **Riscos** e **Plano de entrega**, e essas três seções são justamente o que o doc de design existe pra registrar — o porquê e o que se aceita em troca. Você não me deu essa parte, e eu não vou inventar trade-off, risco ou cronograma. Então deixei as três seções marcadas como pendentes no arquivo e preciso que você responda:

1. **Compensações** — quais foram os custos que vocês aceitaram em troca da melhora na recuperação? Pensando no doc do cache como referência (ele lista ganhos *e* perdas), por exemplo: a busca vetorial fica mais lenta ou mais cara que o `LIKE` exato? Há custo de gerar e manter os embeddings atualizados quando o produto muda? A relevância pode piorar em algum caso (trazer resultado "parecido" mas errado)? O que melhorou e o que piorou?

2. **Riscos** — o que pode dar errado e como vocês pretendem mitigar? Por exemplo: qualidade/relevância do modelo de embeddings; custo de armazenamento e de índice do pgvector com o catálogo inteiro; defasagem dos embeddings em relação ao cadastro; como calibrar o limiar de score que dispara o fallback; carga adicional no Postgres. (O padrão usa uma tabela Risco / Mitigação.)

3. **Plano de entrega** — como vocês querem entregar isso de forma incremental e segura? Por exemplo: backfill dos embeddings do catálogo existente, medição de qualidade (shadow mode comparando com a busca atual? métrica de taxa de "sem resultado"?), e rollout gradual por percentual de tráfego.

Também ficaram em aberto, se você quiser definir agora: quem são os autores e revisores (deixei o estado como **Rascunho**), e o nome do modelo de similaridade de sentenças escolhido. Me responde 1–3 e eu completo o doc.
