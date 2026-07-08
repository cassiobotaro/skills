Criei o rascunho seguindo o padrão dos docs em `docs/design/` (mesmo formato do DD-2026-007: cabeçalho, Resumo, Contexto, Proposta com Compensações, Riscos e Plano de entrega), continuando a sequência de IDs:

**`docs/design/dd-2026-008-busca-por-similaridade-no-catalogo.md`**

O que você me passou preencheu o Resumo, o Contexto e a Proposta: a busca atual por `LIKE`, os ~30% de buscas sem resultado com produto existente, e a solução aprovada no refinamento (embeddings de títulos e descrições com modelo de similaridade de sentenças, armazenamento no pgvector, busca vetorial com fallback pro `LIKE` quando o score vier baixo). Nas Compensações registrei os ganhos que a proposta sustenta — inclusive que o pgvector não adiciona peça nova de infraestrutura.

O nosso template, porém, exige seções que a conversa ainda não preencheu — e eu não vou inventar conteúdo para elas. Deixei cada uma marcada como pendente no doc e preciso das suas respostas para completar:

1. **Autores e revisores** — quem assina o documento, e quais áreas devem revisar? (Alguém de dados/ML pelo modelo de embeddings? Plataforma ou DBA pelo pgvector no Postgres de produção?)

2. **Compensações (os ✗)** — todo design tem custo, e a lista atual só tem ganhos, o que soa como venda. O que piora, encarece ou fica mais arriscado com essa solução? O que o refinamento discutiu como contrapartida (por exemplo: custo/latência de gerar embeddings, dependência de um modelo externo, tamanho do índice)?

3. **Detalhes em aberto da Proposta** — qual modelo de similaridade de sentenças foi escolhido (ou como será escolhido)? Como os embeddings serão atualizados quando um produto mudar de título ou descrição? E qual o limiar de "score baixo" que aciona o fallback — já existe um número ou como ele será calibrado?

4. **Meta mensurável** — dos ~30% de buscas sem resultado, qual é o alvo? Ter um número (ex.: "reduzir para menos de 10%") torna o sucesso verificável e amarra a métrica de acompanhamento.

5. **Riscos** — quais riscos o time levantou e quais mitigações? (O DD-2026-007 usa uma tabela risco → mitigação; sigo o mesmo formato.)

6. **Plano de entrega** — a entrega sai de uma vez ou em fases? Haverá alguma validação antes de 100% (shadow mode, A/B medindo taxa de zero-result) e qual o plano de volta se uma fase der errado?

Com as respostas eu completo as seções pendentes e o doc fica pronto para circular. Se quiser, também posso incluir uma seção de alternativas consideradas (o que mais foi avaliado no refinamento e por que perdeu — incluindo "não fazer nada"): o DD-2026-007 não tem essa seção, mas é ela que torna a decisão auditável daqui a um ano.
