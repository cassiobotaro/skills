Revisei o `docs/design/fanout-de-notificacoes.md`. Apliquei direto o que não dependia de você e listei abaixo o que só você pode responder — hoje o documento descreve bem *o que* será construído, mas quase não registra *por que*: sem trade-offs e alternativas, ele perde o valor no dia em que o código existir.

## O que apliquei

- **Visão geral enxugada**: o parágrafo único misturava contexto atual, proposta e detalhes de implementação (cron, tabela, TPS, DLQ). Agora a visão geral tem duas frases sem detalhe, e os fatos do cenário atual foram para uma nova seção **"Escopo e contexto"** — nada foi inventado, só reorganizado.
- **Glossário no início**: o doc usa CDC, DLQ, TPS, SLA, exchange e fanout sem definir; um revisor de fora do time tropeçaria já na visão geral. Defini os termos padrão de mercado — confira se as definições batem com o uso do time (em especial qual SLA é "o SLA").
- **Texto explicativo após o diagrama**: o fluxograma estava solto. Adicionei um parágrafo nomeando os componentes e como interagem, usando só o que o próprio doc já estabelecia.
- **Abertura da Solução reescrita**: removi "mais escalável e robusta que o modelo atual, além de mais fácil de manter" — adjetivos sem dado de apoio leem como venda, não como decisão. O lugar dessas afirmações é uma seção de trade-offs com prós **e** contras (pergunta 2 abaixo); se houver dado que as sustente, elas voltam com o dado junto.
- **Header**: atualizei "Última atualização" para 2026-07-07.

Mantive sua estrutura, voz e idioma; Objetivos, Fora de escopo e Plano estão intactos porque melhorá-los depende das respostas abaixo.

## Perguntas para você

1. **Template**: o time tem um template de design doc (wiki, drive)? O repositório não mostra nenhum, mas isso é só um indício. Enquanto não houver um confirmado, medi a revisão pelo catálogo padrão — e aí os itens estruturais abaixo são sugestões, não exigências.
2. **Trade-offs da solução** (o achado mais importante): o que piora com o fanout — complexidade operacional de broker + filas + DLQs + CDC, ordenação/duplicação de mensagens, custo de infra? Qual custo o time aceitou, e há algum dado (benchmark, protótipo, número de carga) sustentando os ganhos? Sem uma seção "Trade-offs" com contras explícitos, a solução lê como pitch.
3. **Alternativas consideradas**: o que mais foi avaliado (paralelizar o cron atual? outra forma de ingestão que não CDC?) e por que perdeu? E por que "não fazer nada" não é aceitável — o que acontece se o modelo atual ficar como está?
4. **Objetivos mensuráveis**: "melhorar a performance", "tornar escalável" e "garantir o SLA" não são verificáveis. O que é a "lentidão" hoje em número (latência de entrega? backlog do cron?) e qual é o SLA-alvo (ex.: p99 de entrega em X minutos)?
5. **Fora de escopo real**: "não deve ser lento" e "não deve perder notificações" são objetivos negados, não exclusões — o segundo, aliás, parece um requisito que merece virar objetivo. O que alguém poderia razoavelmente esperar deste trabalho e está deliberadamente excluído (novos canais? preferências de usuário? templates de mensagem)?
6. **DLQ do in-app**: o texto diz "DLQ por canal", mas o diagrama só mostra DLQ para push e e-mail. O in-app ficou sem DLQ de propósito ou é omissão do diagrama?
7. **Times impactados**: quem fora do time é afetado — quem opera o broker, o CDC adiciona carga no banco de origem, os limites de TPS foram combinados com os providers? Isso alimenta uma seção de preocupações transversais e os revisores (com área) que faltam no header.
8. **Verificação e rollback**: como vocês vão comprovar o SLA em produção (métricas, alertas) e, no plano de migração canal a canal, qual é a história de rollback se um canal migrado der errado?

Com as respostas de 2–5 eu preencho as seções correspondentes; 6–8 viram ajustes no diagrama, no header e em seções curtas de fechamento.
