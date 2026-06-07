# DD-2026-008 · Busca por similaridade no catálogo

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | _a definir_ |
| **Revisores** | _a definir_ |
| **Criado em** | 2026-06-07 |
| **Última atualização** | 2026-06-07 |
| **Tags** | catálogo, busca, embeddings, pgvector |

## Glossário

- **Embedding** — representação de um texto como vetor numérico, em que textos com significado próximo ficam próximos no espaço vetorial.
- **Modelo de similaridade de sentenças** — modelo que gera embeddings de frases curtas de forma que a distância entre vetores reflita a proximidade de significado.
- **pgvector** — extensão do Postgres que adiciona um tipo de coluna para vetores e operadores de distância para busca vetorial.
- **Busca vetorial** — recuperação dos itens cujos embeddings estão mais próximos do embedding da consulta, por distância (ex.: cosseno).
- **Score** — medida de proximidade entre a consulta e um resultado; quanto maior, mais semelhante.
- **LIKE** — operador de comparação por padrão de texto do Postgres, usado hoje na busca exata.

## Resumo

A busca do catálogo hoje é por texto exato (`LIKE` no Postgres) e cerca de 30% das buscas terminam sem resultado mesmo quando o produto existe, porque o cliente descreve o produto com palavras diferentes das do título cadastrado. Este documento propõe gerar embeddings dos títulos e descrições dos produtos com um modelo de similaridade de sentenças, armazená-los no pgvector (que já usamos) e fazer busca vetorial, com fallback para o `LIKE` atual quando o score vier baixo.

## Contexto

A busca do catálogo é servida por consultas `LIKE` no Postgres sobre título e descrição dos produtos. Por ser comparação de padrão de texto, ela só encontra o produto quando as palavras digitadas batem com as cadastradas. Hoje cerca de 30% das buscas terminam sem nenhum resultado mesmo com o produto existindo no catálogo: o cliente busca por "tênis de corrida amortecido" e não encontramos o "tênis running com amortecimento", porque nenhum termo coincide. O pgvector já está disponível na nossa instância do Postgres.

## Proposta

Indexar o catálogo por significado, e não só por texto:

1. Para cada produto, concatenar título e descrição e gerar um embedding com um modelo de similaridade de sentenças.
2. Armazenar o embedding em uma coluna pgvector na tabela de produtos (ou tabela associada), mantendo-o atualizado quando título ou descrição mudam.
3. Na busca, gerar o embedding da consulta do cliente e recuperar os produtos mais próximos por distância vetorial, ordenados por score.
4. **Fallback para o `LIKE` atual** quando o melhor score vier abaixo de um limiar: se a busca vetorial não tiver confiança suficiente, cai para o comportamento de hoje, de modo que nenhuma busca fique pior do que está.

A busca exata atual continua existindo como rede de segurança; a busca vetorial entra na frente para recuperar os casos em que hoje não há resultado.

### Compensações

- ✓ Recupera buscas que hoje terminam vazias por diferença de vocabulário entre cliente e cadastro (o caso "tênis de corrida amortecido" → "tênis running com amortecimento").
- ✓ Reaproveita o Postgres/pgvector que já operamos, sem introduzir um novo serviço de busca no caminho crítico.
- ✓ O fallback para `LIKE` garante que, no pior caso, a busca não fica pior do que a de hoje.
- ✗ Passa a existir um modelo de embeddings a operar e versionar: trocar de modelo obriga a regerar os embeddings de todo o catálogo.
- ✗ Os embeddings precisam ser mantidos em dia a cada mudança de título ou descrição — surge um caminho de atualização que hoje não existe.
- ✗ O limiar de score que decide entre busca vetorial e fallback precisa ser calibrado e revisitado; mal ajustado, ou deixa passar resultado ruim, ou descarta bom resultado cedo demais.

## Riscos

| Risco | Mitigação |
|---|---|
| Limiar mal calibrado degrada a qualidade dos resultados | Calibrar com amostra de buscas reais antes do rollout; manter o fallback como piso de qualidade |
| Custo/latência de gerar o embedding da consulta a cada busca | A definir conforme o modelo escolhido — ver questões em aberto |
| Embeddings desatualizados após edição de produto | Regerar o embedding no fluxo de atualização de produto (ver questões em aberto sobre a origem do gatilho) |

## Plano de entrega

1. Gerar embeddings do catálogo existente (backfill) e validar a qualidade da recuperação contra uma amostra de buscas reais — incluindo os ~30% que hoje terminam vazias.
2. Busca vetorial em _shadow mode_, comparando seus resultados com o `LIKE` atual sem afetar o cliente, para calibrar o limiar do fallback.
3. Ativar a busca vetorial com fallback para uma fração do tráfego, depois para 100%, monitorando a taxa de busca sem resultado.

## Questões em aberto

- **Autores e revisores** — quem assina este documento e quais áreas devem revisá-lo (a busca toca Plataforma/dados e possivelmente a equipe de catálogo)?
- **Meta numérica** — qual a redução-alvo da taxa de buscas sem resultado (ex.: dos 30% para abaixo de X%)? Sem um número a meta não é verificável.
- **Qual modelo de similaridade de sentenças** — modelo, dimensão do vetor e onde ele roda (em processo, serviço interno, API externa)? Isso define custo, latência por busca e se há dado saindo da nossa infraestrutura.
- **Onde regerar embeddings** — qual evento/fluxo de atualização de produto dispara a regeração do embedding, e quem é dono desse caminho?
- **Calibração do limiar** — temos uma amostra rotulada de buscas (consulta → produto esperado) para calibrar o limiar e medir a qualidade, ou precisamos construí-la?
- **Alternativas avaliadas no refinamento** — esta proposta foi aprovada no refinamento; quais opções foram descartadas no caminho (ex.: busca textual com sinônimos/`tsvector`/trigram no próprio Postgres, ou um serviço de busca dedicado) e por quê? Registrar isso dá valor de longo prazo ao documento.
