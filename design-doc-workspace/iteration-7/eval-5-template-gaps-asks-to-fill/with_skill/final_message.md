Criei o documento seguindo o padrão dos design docs em `docs/design/` (mesma estrutura do DD-2026-007: cabeçalho, Resumo, Contexto, Proposta com Compensações, Riscos e Plano de entrega), com o próximo número da sequência:

**`docs/design/dd-2026-008-busca-similaridade-catalogo.md`**

O que você me passou preencheu bem o problema (LIKE, ~30% de buscas sem resultado, o exemplo do tênis) e a proposta (embeddings de título e descrição, pgvector, fallback pro LIKE com score baixo) — isso já está escrito. Nas compensações registrei os prós e os custos que decorrem diretamente da própria proposta: manter embeddings sincronizados com o catálogo e passar a operar dois caminhos de busca.

Mas o nosso padrão exige algumas seções que a conversa ainda não preencheu, e eu não vou inventar o conteúdo delas — deixei-as marcadas como pendentes no doc e preciso que você responda:

1. **Cabeçalho** — quem assina como autor(es) e quais áreas devem revisar (ex.: Plataforma, SRE, Dados)?
2. **Proposta (detalhes em aberto)** — qual modelo de similaridade de sentenças vocês vão usar (ou isso ainda está em avaliação)? Os embeddings são gerados na escrita do produto ou em lote? E o limiar de score do fallback já tem valor definido ou será calibrado?
3. **Compensações** — além dos custos que listei, o que mais a equipe aceitou piorar no refinamento (ex.: latência da busca, custo de inferência do modelo)? E existe meta mensurável — reduzir os 30% de buscas sem resultado para quanto?
4. **Riscos** — quais riscos vocês identificaram e como pretendem mitigá-los (ex.: qualidade dos resultados vetoriais, tamanho do índice, backfill dos embeddings do catálogo existente)?
5. **Plano de entrega** — como isso vai a produção: tudo de uma vez ou em etapas (shadow mode, % de tráfego, comparação com a busca atual)?

Com as respostas eu completo as seções pendentes e o doc fica pronto para revisão. Deixei o **Estado** como *Rascunho*: o que foi aprovado no refinamento foi a abordagem, e o documento em si ainda vai passar pelos revisores.
