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

A busca do catálogo hoje é por texto exato (`LIKE` no Postgres) e cerca de 30% das buscas terminam sem resultado mesmo quando o produto existe — o cliente digita "tênis de corrida amortecido" e não encontramos o "tênis running com amortecimento". Este documento propõe gerar embeddings dos títulos e descrições dos produtos com um modelo de similaridade de sentenças, armazená-los no pgvector e fazer a busca vetorial, com fallback para o `LIKE` atual quando o score de similaridade vier baixo.

## Contexto

A busca do catálogo é implementada hoje com `LIKE` no Postgres, casando o termo digitado contra o texto dos produtos. Por depender de correspondência textual, a busca falha quando o cliente usa palavras diferentes das do produto, ainda que descrevam o mesmo item: "tênis de corrida amortecido" não encontra "tênis running com amortecimento". Cerca de 30% das buscas terminam sem nenhum resultado mesmo quando há um produto correspondente no catálogo. O Postgres já é o banco do catálogo e a extensão pgvector já está disponível na nossa instalação.

## Proposta

Indexar o catálogo por similaridade semântica em vez de correspondência textual:

- **Geração de embeddings.** Para cada produto, gerar um embedding a partir do seu título e descrição usando um modelo de similaridade de sentenças.
- **Armazenamento no pgvector.** Guardar o embedding de cada produto numa coluna `vector` no próprio Postgres, usando a extensão pgvector que já utilizamos — sem introduzir um novo banco no caminho.
- **Busca vetorial.** No momento da busca, gerar o embedding do termo digitado e recuperar os produtos mais próximos por similaridade vetorial.
- **Fallback para o `LIKE`.** Quando o score de similaridade da melhor correspondência vetorial vier baixo, recorrer à busca por `LIKE` atual, preservando o comportamento existente como rede de segurança.

### Compensações

> _Pendente da sua resposta — ver as perguntas na conversa._
>
> A proposta troca correspondência textual por similaridade semântica e adiciona
> geração de embeddings e o fallback. O que melhora (e quanto), e o que piora,
> fica mais caro ou mais arriscado em troca, ainda não foi estabelecido — não
> vou inventar números nem custos. Assim que você responder, preencho esta
> subseção no padrão `✓` / `✗` do DD-2026-007.

## Riscos

> _Pendente da sua resposta — ver as perguntas na conversa._
>
> Os riscos desta abordagem (e suas mitigações) ainda não foram levantados.
> Assim que você responder, preencho a tabela Risco / Mitigação no padrão do
> DD-2026-007.

## Plano de entrega

> _Pendente da sua resposta — ver as perguntas na conversa._
>
> A sequência de entrega (backfill dos embeddings do catálogo existente,
> rollout, ativação do fallback, eventual shadow mode) ainda não foi definida.
> Assim que você responder, preencho a lista de fases no padrão do DD-2026-007.
