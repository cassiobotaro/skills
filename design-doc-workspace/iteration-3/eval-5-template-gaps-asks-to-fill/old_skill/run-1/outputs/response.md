Escrevi o design doc seguindo o padrão da pasta `docs/design/` (mesmo cabeçalho, mesmas seções Resumo / Contexto / Proposta com Compensações / Riscos / Plano de entrega, em português, formato enxuto de ~1 página como o DD-2026-007).

Arquivo criado: `docs/design/dd-2026-008-busca-por-similaridade-no-catalogo.md` (continuei a numeração a partir do 007).

O que já dava para escrever com o que você passou: o problema (LIKE, ~30% de buscas vazias, o exemplo do tênis), a proposta (embeddings de título+descrição no pgvector, busca vetorial com fallback pro LIKE) e as compensações que decorrem da própria proposta — o fallback existe justamente porque a busca vetorial tem um custo de confiança, e o modelo de embeddings precisa ser mantido/versionado e regerado quando o produto muda. Acrescentei um glossário (o doc usa bastante vocabulário de domínio: embedding, pgvector, busca vetorial, score) e mantive o formato leve dos docs existentes, sem diagramas.

Não inventei o que não foi estabelecido. Deixei como **questões em aberto** no doc, e preciso da sua resposta para fechá-las:

1. **Autores e revisores** — quem assina e quais áreas revisam? (deixei "_a definir_" no cabeçalho e o estado como "Rascunho")
2. **Meta numérica** — qual a redução-alvo da taxa de buscas sem resultado (dos 30% para abaixo de quanto)? Sem número a meta não é verificável.
3. **Qual modelo de similaridade de sentenças** — qual modelo, qual dimensão de vetor e onde roda (em processo, serviço interno, API externa)? Isso define custo, latência por busca e se sai dado da nossa infra.
4. **Onde os embeddings são regerados** — qual fluxo de atualização de produto dispara a regeração, e quem é dono desse caminho?
5. **Calibração do limiar** — já temos amostra de buscas reais (consulta → produto esperado) para calibrar o limiar e medir qualidade, ou precisamos montar?
6. **Alternativas do refinamento** — a proposta foi aprovada lá; o que foi descartado no caminho (busca textual com sinônimos / `tsvector` / trigram no próprio Postgres, ou um serviço de busca dedicado) e por quê? Registrar isso é o que dá valor de longo prazo ao doc — as compensações ficam mais fortes quando se vê contra o que a opção venceu.

Me responda o que conseguir e eu fecho as seções correspondentes (e mudo o estado de Rascunho para Em revisão).
