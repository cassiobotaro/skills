# DD-2026-008 · Busca por similaridade no catálogo

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | *(pendente — ver perguntas ao autor)* |
| **Revisores** | *(pendente — ver perguntas ao autor)* |
| **Criado em** | 2026-07-07 |
| **Última atualização** | 2026-07-07 |
| **Tags** | catálogo, busca, embeddings, pgvector |

## Resumo

A busca do catálogo compara texto exato (`LIKE` no Postgres) e cerca de 30% das buscas terminam sem resultado mesmo quando o produto existe. Este documento propõe busca por similaridade semântica: gerar embeddings dos títulos e descrições dos produtos com um modelo de similaridade de sentenças, armazená-los no pgvector e consultar por proximidade vetorial, mantendo o `LIKE` atual como fallback quando o score vier baixo.

## Contexto

A busca atual do catálogo é por texto exato, implementada com `LIKE` no Postgres. Cerca de 30% das buscas terminam sem resultado mesmo quando o produto existe no catálogo: o cliente digita "tênis de corrida amortecido" e a busca não encontra o "tênis running com amortecimento", porque nenhuma das palavras bate literalmente. A proposta deste documento foi aprovada no refinamento do time.

## Proposta

O time gera embeddings dos títulos e descrições dos produtos com um modelo de similaridade de sentenças e os armazena no pgvector — extensão do Postgres que o time já usa, portanto sem nova peça de infraestrutura. A busca passa a executar uma consulta vetorial: o serviço gera o embedding do termo digitado pelo cliente e busca os produtos mais próximos no espaço vetorial. Quando o score de similaridade vier baixo, a busca cai no fallback: a consulta `LIKE` atual, preservando o comportamento de hoje.

Três pontos da proposta ainda não foram definidos e estão em aberto (ver perguntas ao autor): o modelo de embeddings, a estratégia de atualização dos vetores quando um produto muda de título ou descrição, e o limiar que define "score baixo" para acionar o fallback.

### Compensações

- ✓ A busca passa a encontrar produtos descritos com outras palavras ("tênis de corrida amortecido" encontra "tênis running com amortecimento"), atacando os ~30% de buscas sem resultado
- ✓ pgvector é extensão do Postgres já em uso — nenhum banco ou serviço novo na infraestrutura
- ✓ O fallback para o `LIKE` preserva o comportamento atual quando a similaridade não dá resposta confiável
- ✗ *(pendente — o refinamento não registrou os custos aceitos; uma lista de compensações sem ✗ não está completa. Ver perguntas ao autor.)*

## Riscos

*(pendente — riscos e mitigações não foram levantados na conversa; ver perguntas ao autor.)*

## Plano de entrega

*(pendente — a segmentação da entrega não foi definida na conversa; ver perguntas ao autor.)*
