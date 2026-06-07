Criei o rascunho seguindo o padrão dos design docs em `docs/design/`, no mesmo template do `DD-2026-007` (Resumo → Contexto → Proposta com subseção Compensações → Riscos → Plano de entrega):

`docs/design/dd-2026-008-busca-por-similaridade-no-catalogo.md`

O que você me passou já preencheu **Resumo**, **Contexto** e **Proposta** (incluindo o fallback para o `LIKE`). Faltam três seções que o template exige e cujo conteúdo só você tem — deixei cada uma marcada como _pendente da sua resposta_ no doc, sem inventar nada. Para preenchê-las:

**Compensações** — Toda decisão tem um custo, e a proposta troca correspondência textual por similaridade semântica.
1. Qual o ganho esperado e como vocês o medem? (Ex.: derrubar a taxa de "sem resultado" dos ~30% atuais para quanto? Há prova de conceito com algum número de recall ou de buscas recuperadas?)
2. O que piora ou fica mais caro em troca? Penso em: latência por gerar o embedding do termo a cada busca, custo/operação do modelo de similaridade, e relevância "fuzzy" demais trazendo resultados parecidos mas errados. Algum desses pesa, ou há outro custo que vocês já aceitaram?

**Riscos** — No padrão Risco / Mitigação do DD-2026-007:
3. Quais riscos vocês veem nesta abordagem e como mitigá-los? Candidatos: embeddings ficarem defasados quando título/descrição do produto mudam (como reindexar?); qualidade ruim numa categoria específica; o modelo de similaridade indisponível (o fallback para `LIKE` cobre isso totalmente?); custo de armazenamento/índice do pgvector com o catálogo inteiro.

**Plano de entrega** — No padrão de fases do DD-2026-007:
4. Como isso vai para produção? Em particular: existe um backfill dos embeddings do catálogo já existente? Há shadow mode / ativação por porcentagem de tráfego como no cache (DD-2026-007)? Qual a história de rollback se a busca vetorial piorar a relevância?

E duas do cabeçalho, para fechar o doc:
5. Quem são os autores e quais áreas/times devem revisar (Plataforma? SRE? Dados/ML pelo modelo de embeddings)?

Respondendo essas, eu preencho as três seções pendentes e o cabeçalho mantendo o estilo do DD-2026-007.
