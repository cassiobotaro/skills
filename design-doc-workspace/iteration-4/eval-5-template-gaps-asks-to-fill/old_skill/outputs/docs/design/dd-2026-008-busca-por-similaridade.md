# DD-2026-008 · Busca por similaridade no catálogo

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | _(a preencher)_ |
| **Revisores** | _(a preencher)_ |
| **Criado em** | 2026-06-07 |
| **Última atualização** | 2026-06-07 |
| **Tags** | catálogo, busca, embeddings, pgvector |

## Resumo

A busca do catálogo é hoje por texto exato (`LIKE` no Postgres) e cerca de 30% das buscas terminam sem resultado mesmo quando o produto existe, porque o cliente descreve o produto com palavras diferentes das do título. Este documento propõe gerar embeddings dos títulos e descrições dos produtos com um modelo de similaridade de sentenças, armazená-los no pgvector e fazer a busca vetorial, com fallback para o `LIKE` atual quando o score de similaridade vier baixo.

## Contexto

A busca atual casa o termo do cliente contra os campos do produto usando `LIKE` no Postgres, ou seja, exige correspondência de texto. Quando o cliente descreve o produto com outras palavras que não as do cadastro, a busca não encontra: o cliente digita "tênis de corrida amortecido" e não recuperamos o "tênis running com amortecimento". Cerca de 30% das buscas terminam sem resultado mesmo quando o produto existe no catálogo. A extensão pgvector já está disponível no Postgres que usamos hoje.

## Proposta

Gerar embeddings dos títulos e descrições dos produtos com um modelo de similaridade de sentenças e armazená-los no pgvector (extensão do Postgres que já usamos). A busca passa a ser vetorial: o termo do cliente é convertido em embedding e comparado por similaridade contra os embeddings dos produtos. Quando o score de similaridade da melhor correspondência vier baixo, a busca faz fallback para o `LIKE` atual, preservando o comportamento existente nos casos em que a busca vetorial não tem confiança suficiente.

### Compensações

_(pendente — preciso da sua resposta; ver pergunta 1 na conversa. O padrão da casa exige esta seção e ela não deve ser inventada.)_

## Riscos

_(pendente — preciso da sua resposta; ver pergunta 2 na conversa. O padrão da casa exige esta seção e ela não deve ser inventada.)_

## Plano de entrega

_(pendente — preciso da sua resposta; ver pergunta 3 na conversa. O padrão da casa exige esta seção e ela não deve ser inventada.)_
