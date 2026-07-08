Revisão concluída. Segue, na íntegra, a resposta que eu daria ao usuário:

---

Revisei o documento e apliquei direto o que não dependia de você. O que falta são justamente as partes que só você pode responder — e são as mais valiosas do doc.

## Perguntas para você

1. **Template**: o time tem um template de design doc (wiki, drive)? Não há outro design doc no repositório para comparar, então revisei contra um catálogo padrão — se existir um template oficial, ele passa a mandar e eu reavalio as seções.
2. **Trade-offs da solução** (o achado mais importante): o doc apresenta o fanout só com vantagens — "mais escalável e robusta, mais fácil de manter" é discurso de venda, não decisão de engenharia. O que **piora** em troca? Por exemplo: complexidade operacional do broker, entrega at-least-once/duplicatas, perda de ordenação, infraestrutura nova para operar. Quais desses custos o time aceitou?
3. **Alternativas consideradas**: o que mais foi avaliado antes do fanout — paralelizar dentro do serviço atual, escalar o cron, algum serviço gerenciado? E por que **não fazer nada** não é aceitável? Sem isso a decisão não é auditável depois.
4. **Números**: "melhorar a performance", "tornar escalável" e "garantir o SLA" não são verificáveis. Quão lento está hoje (volume, atraso, latência)? Qual é o valor do SLA e como ele é medido? Qual meta numérica diria que o projeto deu certo?
5. **Fora de escopo real**: "não deve ser lento" e "não deve perder notificações" eram requisitos, não exclusões (movi o segundo para os objetivos; o primeiro já era o objetivo de performance). O que alguém poderia razoavelmente esperar deste trabalho e **não** será feito?
6. **DLQ do in-app**: o texto diz "DLQ por canal", mas o diagrama não tem DLQ para o worker de in-app. Qual dos dois vale? Não corrigi o diagrama para não decidir por você.
7. **Impactados e revisores**: quem fora do Time de Mensageria é afetado (infra do broker, limites de TPS dos providers)? Sugiro nomeá-los como revisores no cabeçalho e, com sua resposta, adicionar uma seção de preocupações transversais.

## Edições aplicadas em `docs/design/fanout-de-notificacoes.md`

1. **Visão geral enxuta + nova seção "Escopo e contexto"**: a visão geral tinha um parágrafo único com todos os detalhes (cron, tabela, mecanismo inteiro da solução). Agora ela diz em duas frases o problema e a proposta; o funcionamento atual foi movido para "Escopo e contexto".
2. **Glossário no início**: o doc usa CDC, DLQ, TPS, SLA, exchange, fanout, in-app e provider sem definir — um revisor de outro time tropeçaria em todos. Defini cada um em uma linha.
3. **Texto explicativo após o diagrama**: o fluxograma estava solto. Adicionei um parágrafo que nomeia os componentes e descreve o fluxo (CDC → dispatcher → exchange → filas → workers → providers/DLQ), usando só o que o doc já estabelecia.
4. **Removi o discurso de venda**: cortei "mais escalável e robusta que o modelo atual, além de mais fácil de manter" — afirmações vagas sem dado de suporte. O lugar delas é uma seção de trade-offs com prós **e** contras, que adiciono quando você responder a pergunta 2.
5. **Objetivos**: "não perder notificações" saiu de fora de escopo (era um requisito) e virou objetivo; "Garantir o SLA" virou "Garantir o SLA de entrega". As metas continuam sem número — depende da pergunta 4.
6. **Fora de escopo**: ficou marcado como "a definir" apontando para as questões em aberto, em vez de manter exclusões que só negavam os objetivos.
7. **Nova seção "Questões em aberto"**: registra no próprio doc as pendências acima (números, SLA, trade-offs, alternativas, DLQ do in-app, times impactados) — honestidade que convida à colaboração em vez de esconder o que falta.
8. **Cabeçalho**: "Última atualização" passou para 2026-07-07.

## Sugestões (não apliquei)

- Quando você responder as perguntas 2 e 3, adiciono as seções **"Trade-offs da solução escolhida"** e **"Alternativas consideradas"** — são elas que dão valor de longo prazo ao documento.
- O diagrama de arquitetura poderia ser autorado como Structurizr DSL (C4) com a imagem renderizada no doc e o fonte dobrado num `<details>`, em vez de flowchart Mermaid. É opcional; mantive seu diagrama como está.
- O plano de migração poderia indicar o critério para avançar de etapa (ex.: o que precisa ser verdade no canal de e-mail antes de migrar push e in-app) e se há rollback — me diga se existe e eu incluo.
