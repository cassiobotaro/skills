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

Cerca de 30% das buscas no catálogo terminam sem resultado mesmo quando o produto existe, porque a busca atual compara texto exato. Este documento propõe a busca por similaridade aprovada no refinamento: gerar embeddings dos títulos e descrições dos produtos com um modelo de similaridade de sentenças, armazená-los no pgvector e buscar por proximidade vetorial, com fallback para o LIKE atual quando o score vier baixo.

## Contexto

A busca do catálogo hoje é por texto exato, implementada com LIKE no Postgres. Isso exige que o termo digitado pelo cliente coincida literalmente com o texto cadastrado no produto: quem busca "tênis de corrida amortecido" não encontra o "tênis running com amortecimento", ainda que seja exatamente o produto procurado. Cerca de 30% das buscas terminam sem resultado mesmo quando o produto existe no catálogo.

O catálogo roda sobre Postgres, e o pgvector — a extensão do Postgres para armazenamento e busca de vetores — já faz parte da nossa instalação.

## Proposta

Para cada produto, geramos um embedding — um vetor numérico que representa o significado do texto — a partir do título e da descrição, usando um modelo de similaridade de sentenças, e o armazenamos no pgvector. Na busca, convertemos o termo digitado pelo cliente em embedding com o mesmo modelo e consultamos os produtos mais próximos por similaridade vetorial. Quando o score do melhor resultado vem abaixo do limiar, a busca cai para o LIKE atual (fallback), preservando o comportamento de hoje como piso.

O modelo de similaridade a usar, o momento de geração dos embeddings (na escrita do produto ou em lote) e o valor do limiar de score ainda não foram definidos — ver perguntas ao autor.

### Compensações

- ✓ Encontra produtos pelo significado, não pelo casamento exato de texto — ataca diretamente os ~30% de buscas sem resultado com produto existente (o caso "tênis de corrida amortecido" → "tênis running com amortecimento")
- ✓ pgvector é extensão do Postgres que já usamos: a busca vetorial não adiciona uma nova peça de infraestrutura
- ✗ Os embeddings precisam acompanhar o catálogo: toda criação ou edição de título/descrição exige (re)gerar o embedding do produto
- ✗ Passam a existir dois caminhos de busca (vetorial + LIKE de fallback) para manter e monitorar, incluindo a calibração do limiar de score que decide entre eles

## Riscos

*Pendente — a equipe ainda não registrou os riscos e mitigações desta mudança (ver perguntas ao autor).*

## Plano de entrega

*Pendente — as etapas de entrada em produção ainda não foram definidas (ver perguntas ao autor).*
