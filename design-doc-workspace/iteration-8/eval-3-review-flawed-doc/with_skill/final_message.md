Revisei o `docs/design/fanout-de-notificacoes.md`. Como não encontrei outros design docs no repositório nem um template confirmado, medi contra um catálogo padrão de seções — então as observações estruturais abaixo são sugestões, não exigências (a primeira pergunta é justamente sobre isso). Apliquei direto o que não dependia de você e deixei o resto como perguntas.

## O que apliquei

- **Visão geral enxugada.** Ela misturava a descrição detalhada do modelo atual (cron, tabela `notifications`, providers um a um) com detalhes da solução (DLQ, TPS, CDC). Agora é um parágrafo sem detalhes: o problema e o tipo de solução proposta.
- **Nova seção "Escopo e contexto".** O detalhe do funcionamento atual saiu da visão geral e virou contexto — fatos que situam o leitor, sem decisão no meio.
- **Glossário logo após o cabeçalho.** O doc usa CDC, DLQ, SLA e TPS sem definir; um revisor de fora do time tropeçaria. Defini cada um em uma linha.
- **Texto explicativo depois do diagrama.** O diagrama estava sozinho; adicionei um parágrafo (só com o que o próprio doc já estabelecia) nomeando os componentes e dizendo como interagem: CDC → dispatcher → exchange → filas por canal → workers → providers com limite de TPS → DLQ.
- **Removi o discurso de venda da Solução.** "Mais escalável e robusta, além de mais fácil de manter" são adjetivos que não sobrevivem ao "por quê?" de um revisor — esse conteúdo pertence a uma seção de trade-offs com fatos por trás (pergunta 2 abaixo).
- **Cabeçalho:** atualizei "Última atualização" para 2026-07-07.

## O que preciso de você

1. **Template:** vocês têm um template de design doc do time/empresa (wiki, drive)? Se houver, ele passa a mandar na estrutura e eu reviso os itens abaixo contra ele.
2. **Trade-offs da solução escolhida** — a lacuna mais importante: o doc só apresenta ganhos. O que piora ou fica mais caro com o fanout (operar broker/filas/CDC, mais partes móveis, ordenação/duplicação de eventos…)? Qual custo o time aceitou? E que dado sustenta os ganhos (benchmark, número de carga)?
3. **Alternativas consideradas:** o que mais foi avaliado, incluindo "não fazer nada" — por que otimizar o modelo atual (por exemplo, paralelizar o cron) não basta?
4. **Objetivos mensuráveis:** "melhorar a performance", "tornar escalável" e "garantir o SLA" não são verificáveis. Qual é o SLA de entrega (número)? Qual a latência/volume de hoje e qual o alvo?
5. **Fora de escopo real:** os dois itens atuais ("não deve ser lento", "não deve perder notificações") só negam os objetivos — são requisitos, não exclusões. O que fica de fora de verdade (novos canais? troca de providers? preferências do usuário?)?
6. **DLQ do in-app:** o texto diz "DLQ por canal", mas o diagrama não tem DLQ para o worker in-app. É proposital (in-app não chama provider externo?) ou faltou no diagrama?
7. **Revisores e times impactados:** quem revisa este doc, com que área (infra do broker, banco/CDC, times dos providers)? Com as respostas dá para preencher o cabeçalho e uma seção de preocupações transversais.
8. **Plano:** existe critério para avançar de fase (por exemplo, e-mail estável por N dias) e caminho de rollback se uma etapa der errado?

Com as respostas de 2–5 eu adiciono as seções de Trade-offs e Alternativas e corrijo Objetivos/Fora de escopo — são elas que dão valor de longo prazo ao documento.
