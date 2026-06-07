Escrevi o rascunho em `docs/design/dd-2026-008-busca-por-similaridade-no-catalogo.md`, seguindo o mesmo formato do DD-2026-007 (Resumo → Contexto → Proposta → Compensações → Riscos → Plano de entrega) e continuando a numeração (DD-2026-008). Acrescentei só um Glossário no início, porque este doc usa bem mais jargão (embedding, pgvector, busca vetorial) que o de cache — se preferir manter idêntico ao 007, eu removo.

Preenchi com o que você passou: o problema (LIKE/texto exato, ~30% de buscas vazias, o exemplo do "tênis de corrida amortecido" vs. "tênis running com amortecimento"), o contexto (Postgres + pgvector já em uso) e a proposta (embeddings de título/descrição, armazenados no pgvector, busca vetorial com fallback pro LIKE quando o score for baixo).

O que **não** preenchi, porque seria inventar — e num design doc as compensações e os riscos são justamente o que dá valor ao documento. Deixei cada lacuna marcada com a pergunta no próprio lugar. Para fechar o doc, preciso de você:

**Compensações (o custo aceito — sem isso vira folheto de vendas):**
1. O que ficou pior/mais arriscado/mais caro em troca de recuperar as buscas? Qual o custo de latência da busca vetorial + geração do embedding da consulta, comparado ao LIKE de hoje? E o custo de manter os embeddings atualizados e reindexar o catálogo existente? Quanto de resultado irrelevante (falso positivo) a busca vetorial pode trazer que o LIKE exato não traria?

**Proposta (detalhes que mudam o desenho):**
2. Qual modelo de similaridade de sentenças, e onde ele roda — serviço próprio, biblioteca embarcada ou API externa?
3. Qual o limiar de score que aciona o fallback pro LIKE, e como ele foi escolhido?
4. O resultado é só a busca vetorial (com fallback), ou os dois caminhos são combinados/reordenados?

**Riscos + mitigações:**
5. Quais riscos a equipe enxerga (qualidade/ranqueamento errado, latência no pico, defasagem dos embeddings após mudança de catálogo ou troca de modelo, carga extra no Postgres) e como mitigar cada um?

**Plano de entrega:**
6. A geração dos embeddings do catálogo atual é um backfill único antes de ativar? Entra atrás de flag/percentual como no DD-2026-007? Tem etapa de medição (ex.: comparar recall vetorial vs. LIKE em shadow) antes de ir pro cliente? Qual a história de rollback se a qualidade piorar?

**Header:**
7. Quem são os autores e quais áreas devem revisar? Sugeri Plataforma/banco (dono do pgvector) e SRE (capacidade e latência) — confirma ou ajusta.

Sobre meta mensurável: usei as ~30% de buscas vazias como número de sucesso no Resumo (o 007 também não tem seção própria de metas, mantém o número no texto). Se quiser um alvo explícito — por exemplo "reduzir buscas vazias de 30% para X%" — me diz o X que eu registro.

Me responda o que conseguir dessas que eu completo o documento; o que não tiver resposta ainda, movo pra uma seção de Pendências em vez de inventar.
