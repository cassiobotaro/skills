Li o `docs/design/dd-2026-007-cache-de-catalogo.md` para pegar o padrão da casa. A estrutura que ele estabelece é:

tabela de cabeçalho (Documento, Estado, Autores, Revisores, Criado em, Última atualização, Tags) → **Resumo** → **Contexto** → **Proposta** com uma subseção **### Compensações** (`✓` / `✗`) → **Riscos** (tabela Risco | Mitigação) → **Plano de entrega** (lista numerada de fases).

Vou seguir esse formato exatamente, em `docs/design/dd-2026-008-busca-por-similaridade.md` (continuando a numeração).

O que você já me deu cobre bem o Resumo, o Contexto e o miolo da Proposta: busca por `LIKE` hoje, ~30% das buscas terminando sem resultado, embeddings de título e descrição, armazenamento no pgvector (extensão que já roda no nosso Postgres) e fallback pro `LIKE` quando o score vier baixo.

Antes de escrever, preciso de cinco coisas que só o time tem — três delas são seções que o template exige e que eu não vou preencher com achismo:

1. **Compensações (obrigatória no template).** A proposta chegou só com o lado bom, e isso é o sinal de alerta clássico: o que a busca vetorial piora? Latência da consulta comparada ao `LIKE`? Custo e tempo de gerar/reindexar os embeddings quando o catálogo muda? Memória e tamanho do índice no Postgres? Resultados aproximados demais chegando pro cliente (falso positivo, que hoje não existe)? Qual desses o time decidiu aceitar conviver?

2. **Riscos e mitigações (obrigatória no template).** O que pode dar errado na operação — carga da geração de embeddings no banco, indisponibilidade do modelo, qualidade ruim em categorias específicas, produtos novos sem embedding — e o que vocês fariam pra mitigar cada um? O DD-2026-007 lista dois riscos com mitigação; me dá os equivalentes aqui.

3. **Plano de entrega (obrigatória no template).** Isso vai em etapas (shadow mode medindo a taxa de busca sem resultado, percentual de tráfego, categoria piloto) ou entra de uma vez? E existe caminho de volta se uma etapa der errado?

4. **Cabeçalho.** Quem assina como autor, quem revisa (com a área, no padrão "João Prata (Plataforma)") e em que estado o doc entra — "aprovado no refinamento" quer dizer **Aprovado**, ou ele ainda passa por revisão como **Em revisão**?

5. **Dois detalhes da proposta que não quero inventar.** Qual modelo de similaridade de sentenças e onde a inferência roda — em batch na indexação e também online na consulta do cliente? E qual é o score de corte que dispara o fallback pro `LIKE`, ou isso ainda está em aberto? Aproveitando: os 30% de buscas sem resultado caem pra quanto — vocês têm uma meta medida?

Responde o que tiver; o que ficar sem resposta eu registro como pergunta em aberto em vez de preencher com texto genérico. Assim que você responder eu escrevo o documento inteiro, incluindo o diagrama de fluxo da busca (consulta → vetorial → fallback) e o diagrama de contêineres do C4 se você quiser que ele entre.
