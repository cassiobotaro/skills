O design doc está em `docs/design/webhooks-de-saida.md`, em português. Os dois diagramas estão no texto, mas o de arquitetura ainda não virou imagem.

**O que o documento traz**
- Glossário, visão geral, contexto, objetivos, o design, trade-offs, alternativas e questões em aberto.
- Em alternativas entram "não fazer nada" (descartada pela dor que você descreveu), o SaaS (custo por evento e payload fora da borda) e a solução escolhida.
- O custo aceito, a entrega deixar de ser imediata em alguns casos, está nos trade-offs e na visão geral.
- O fluxo de entrega com retry é um diagrama Mermaid, seguido de texto explicativo.

**Diagrama de arquitetura**
- Como não há Docker nem a CLI do Structurizr, o diagrama é um DSL dobrado em `<details>`.
- A referência da imagem aponta para `diagrams/architecture.svg`, que ainda não existe.
- Falta renderizar o SVG e salvá-lo em `docs/design/diagrams/`.
- Não validei o DSL, porque não há ferramenta para isso aqui.

**Questões em aberto**
Não inventei nada que você não tinha dito. O que faltava virou item na seção final:
- metas mensuráveis e o que fica fora de escopo;
- em quais casos a entrega deixa de ser imediata, e qual atraso é aceitável;
- intervalos do backoff, timeout e o critério que classifica uma resposta como falha;
- o que dispara os retries;
- onde a DLQ vive e se há replay;
- semântica de duplicatas e deduplicação pelo cliente;
- gestão e rotação dos segredos HMAC, e os cabeçalhos da assinatura;
- quem consulta o log de tentativas e por quanto tempo ele é retido;
- impacto em outras equipes.

Por isso, o diagrama de arquitetura não mostra a DLQ nem o mecanismo de retry, e as tecnologias que aparecem são só Kafka, Postgres e HMAC.

O cabeçalho deixa autores e revisores como "A definir". Me diga quem são e quais áreas devem revisar (segurança e plataforma, por exemplo). Passei o `unslop` na prosa e não cometi nenhum commit.
