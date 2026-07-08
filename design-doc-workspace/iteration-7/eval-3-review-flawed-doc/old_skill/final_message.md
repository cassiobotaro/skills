Revisei o doc e apliquei direto o que não dependia de você. Segue a revisão completa.

---

Li o `docs/design/fanout-de-notificacoes.md` inteiro. A estrutura geral está boa (cabeçalho, visão geral, objetivos, escopo, solução com diagrama, plano) e o texto é direto. Os problemas mais importantes são de substância — decisões sem custo declarado e sem alternativas — e esses só você pode responder. Separei em dois grupos.

## Perguntas pra você responder

Estas são as lacunas de maior valor do doc; sem elas, o documento perde o valor assim que o código existir. Não preenchi nada disso com placeholder — entra no doc só com as suas respostas:

1. **Trade-offs da solução escolhida (a lacuna mais importante).** Hoje a solução aparece só com vantagens ("mais escalável e robusta… mais fácil de manter") — sem nenhum custo, isso lê como pitch de vendas, não como decisão. O que piorou em troca? Por exemplo: complexidade operacional de um broker novo, entrega at-least-once (duplicatas? os providers/handlers são idempotentes?), perda de ordenação, latência do CDC, mais peças pra monitorar. E há algum fato/número sustentando "mais escalável" (benchmark, protótipo, carga atual vs. projetada)?
2. **Alternativas consideradas — incluindo "não fazer nada".** O que mais o time avaliou? (ex.: paralelizar os envios dentro do próprio serviço, escalar o cron/particionar a tabela, usar um serviço gerenciado de mensageria.) E por que continuar como está não é aceitável — qual o tamanho da lentidão hoje?
3. **Objetivos mensuráveis.** "Melhorar a performance", "tornar escalável" e "garantir o SLA" não são verificáveis. Qual é o SLA de entrega (número)? Qual a latência/vazão hoje e qual o alvo? Com números, dá pra saber se o projeto funcionou.
4. **Fora de escopo real.** Os dois itens atuais só negam os objetivos ("não deve ser lento", "não deve perder notificações") — isso não exclui nada. O que de fato fica de fora que alguém poderia esperar? (ex.: novos canais como SMS/WhatsApp, reprocessamento automático da DLQ, notificações em tempo real.) Aliás, "não perder notificações" parece ser um **requisito** da solução, não um fora de escopo — deveria virar objetivo?
5. **Impactados e infraestrutura.** Qual broker será usado e quem o opera? Quem fora do time de Mensageria é impactado — time de banco de dados (CDC), infra, os limites de TPS dos providers? Esses times deveriam entrar como revisores no cabeçalho (hoje o doc está "Em revisão" sem nenhum revisor nomeado).
6. **DLQ do canal in-app.** O texto diz "DLQ por canal", mas o diagrama só mostra DLQ para push e e-mail. É intencional (falha de in-app é barata/regravável) ou faltou no diagrama? Confirmando, eu ajusto o diagrama ou o texto.
7. **Dados sensíveis.** O payload das notificações carrega PII (nome, e-mail, telefone)? Isso vai parar nas filas e DLQs e restringe retenção/criptografia — vale uma linha no doc.
8. **Plano e rollback.** Durante a migração por canal, cron e fanout convivem — como se evita envio duplicado? E se uma etapa der errado, qual o caminho de volta antes de "desligar o cron"?

Com as respostas de 1 e 2 eu adiciono as seções **"Trade-offs da solução"** e **"Alternativas consideradas"**; com 5, 7 e 8, uma seção curta de **"Preocupações transversais"** e o detalhamento do plano também fariam sentido — mas só se você tiver o conteúdo.

## Edições que já apliquei

1. **Glossário no início do documento** — o doc usa CDC, DLQ, SLA e TPS sem definir; um revisor de fora tropeçaria em todos. Defini os quatro (definições padrão dos termos; me corrija se algum tiver sentido específico no seu contexto).
2. **Visão geral enxuta, contexto separado** — a visão geral misturava o estado atual detalhado (cron, tabela `notifications`, providers um a um) com detalhes da solução (DLQ, TPS, CDC). Deixei a visão geral em um parágrafo sem detalhes e movi o estado atual para uma nova seção **"Contexto"**; os detalhes da solução desceram para a seção "Solução". Nada foi inventado — só reorganizei o que você já tinha escrito.
3. **Texto explicativo após o diagrama** — o fluxograma estava solto; adicionei um parágrafo nomeando os componentes e explicando o fluxo (CDC → dispatcher → exchange → filas por canal → workers → DLQ), usando apenas o que o próprio doc já estabelecia.
4. **"Última atualização" do cabeçalho** — atualizei para 2026-07-07, data desta revisão.

Não mexi em Objetivos, Fora de escopo, na afirmação "mais escalável e robusta" nem no diagrama (a DLQ de in-app): tudo isso depende das suas respostas acima. Me manda o que tiver e eu completo o documento.
