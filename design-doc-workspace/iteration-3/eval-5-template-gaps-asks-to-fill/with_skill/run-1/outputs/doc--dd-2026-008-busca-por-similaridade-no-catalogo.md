# DD-2026-008 · Busca por similaridade no catálogo

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | _A preencher_ |
| **Revisores** | _A preencher (sugestão: Plataforma/banco — dono do pgvector; SRE — capacidade e latência)_ |
| **Criado em** | 2026-06-07 |
| **Última atualização** | 2026-06-07 |
| **Tags** | catálogo, busca, embeddings, pgvector |

## Glossário

| Termo | Definição |
|---|---|
| Embedding | Vetor numérico que representa o significado de um texto, de forma que textos parecidos ficam próximos no espaço vetorial. |
| pgvector | Extensão do Postgres para armazenar embeddings e consultar por proximidade (já em uso no projeto). |
| Modelo de similaridade de sentenças | Modelo que transforma uma frase em um embedding pensado para comparar significado entre frases. |
| Busca vetorial | Busca que ordena resultados pela proximidade do embedding da consulta aos embeddings dos produtos. |
| LIKE | Busca por correspondência de texto literal no Postgres, usada hoje no catálogo. |
| Score | Medida de proximidade entre o embedding da consulta e o do produto; quanto maior, mais semelhante. |

## Resumo

A busca do catálogo hoje é por texto exato (`LIKE` no Postgres) e cerca de 30% das buscas terminam sem resultado mesmo quando o produto existe, porque o cliente e o cadastro descrevem o mesmo item com palavras diferentes. Este documento propõe gerar embeddings dos títulos e descrições dos produtos com um modelo de similaridade de sentenças, armazená-los no pgvector (extensão do Postgres que já usamos) e fazer a busca por similaridade vetorial, mantendo o `LIKE` atual como fallback quando o score da busca vetorial vier baixo.

## Contexto

A busca do catálogo é implementada hoje com `LIKE` no Postgres, ou seja, casa apenas correspondências de texto literal entre o termo digitado e o título/descrição do produto. Como cliente e cadastro frequentemente descrevem o mesmo item com vocabulário diferente — o cliente digita "tênis de corrida amortecido" e o produto está cadastrado como "tênis running com amortecimento" —, cerca de 30% das buscas terminam sem nenhum resultado mesmo quando o produto existe no catálogo.

Já usamos Postgres como banco do catálogo e já temos a extensão pgvector disponível, o que torna a busca vetorial viável sem introduzir uma nova peça de infraestrutura. A abordagem por embeddings foi a proposta aprovada no refinamento da equipe.

## Proposta

Indexar o catálogo por similaridade semântica e usar essa similaridade como caminho principal da busca, caindo para o `LIKE` atual quando a busca vetorial não tiver confiança suficiente:

- **Geração de embeddings**: para cada produto, gerar um embedding a partir do título e da descrição usando um modelo de similaridade de sentenças. O embedding é (re)gerado quando o produto é criado ou atualizado.
- **Armazenamento**: guardar o embedding no próprio Postgres, em coluna `vector` do pgvector, ao lado do produto, com índice de proximidade para consulta eficiente.
- **Busca**: na consulta, gerar o embedding do termo digitado e buscar os produtos mais próximos por similaridade vetorial.
- **Fallback**: quando o score da melhor correspondência vetorial vier abaixo de um limiar, recorrer à busca `LIKE` atual, preservando o comportamento de hoje para os casos em que a busca vetorial não ajuda.

> _A detalhar com o autor — itens da proposta ainda não estabelecidos:_
> - _Qual modelo de similaridade de sentenças será usado e onde ele roda (serviço próprio, biblioteca embarcada, API externa)?_
> - _Qual o limiar de score que dispara o fallback para o `LIKE`, e como ele foi escolhido?_
> - _O resultado é só a busca vetorial (com fallback), ou os dois caminhos são combinados/reordenados?_

### Compensações

> _A preencher com o autor — esta seção é o cerne do documento e não pode ser inventada._
> A proposta tem ganho claro (recuperar parte das ~30% de buscas vazias), mas os custos aceitos
> ainda não foram estabelecidos. Perguntas para o autor:
> - _O que ficou pior, mais arriscado ou mais caro em troca do ganho de recall?_
> - _Qual o custo de latência da busca vetorial mais a geração do embedding da consulta, comparado ao `LIKE` atual?_
> - _Qual o custo de manter os embeddings atualizados (reprocessamento em criação/atualização de produto) e de reindexar o catálogo já existente?_
> - _Quanto a busca vetorial pode trazer resultado irrelevante (falsos positivos) que o `LIKE` exato não traria?_

- ✓ Recupera buscas hoje vazias quando o produto existe mas usa vocabulário diferente do termo digitado (alvo das ~30%).
- ✓ Reaproveita Postgres e pgvector, já em uso — sem nova peça de infraestrutura no caminho da busca.
- ✗ _A preencher com o autor (ver perguntas acima)._

## Riscos

> _A preencher com o autor — riscos e mitigações ainda não foram estabelecidos._
> Pontos a confirmar para preencher a tabela:
> - _Qualidade dos resultados: a busca vetorial pode ranquear bem produtos semanticamente próximos porém errados (ex.: tênis casual para "tênis de corrida"). Como medir e mitigar?_
> - _Custo/latência da geração de embedding na consulta sob pico de tráfego. Mitigação?_
> - _Defasagem dos embeddings após mudança de catálogo ou troca do modelo (necessidade de reindexação). Mitigação?_
> - _Carga adicional no Postgres pela busca vetorial e pelo índice. Mitigação?_

| Risco | Mitigação |
|---|---|
| _A preencher_ | _A preencher_ |

## Plano de entrega

> _A preencher com o autor — a sequência de entrega ainda não foi estabelecida._
> Perguntas para definir as fases:
> - _A geração de embeddings do catálogo existente é um backfill único antes de ativar a busca? Quanto tempo/qual carga isso impõe?_
> - _A busca vetorial entra atrás de flag/percentual de tráfego, como no DD-2026-007, ou de uma vez?_
> - _Há etapa de medição (ex.: comparar recall vetorial vs. `LIKE` em shadow) antes de ativar para clientes?_
> - _Qual a história de rollback se a qualidade dos resultados piorar?_

1. _A preencher_
