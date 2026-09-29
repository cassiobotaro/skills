Revisei o `docs/design/fanout-de-notificacoes.md`. Apliquei direto o que era clareza e estrutura; o que é substância só você consegue responder, e está listado abaixo. Nada foi inventado para preencher lacuna: onde faltava fato, ficou pergunta.

## Perguntas para você

1. **Template da casa.** O time segue algum modelo de design doc (wiki, drive)? Se sim, me passa a referência: as sugestões abaixo ficam mais úteis nos termos dele. Se não existe, tudo bem, sigo com o vocabulário padrão.

2. **Números.** "Começou a apresentar lentidão" e os três objetivos (performance, escalável, SLA) não têm como ser verificados. Qual é o volume e a latência hoje, e qual número define sucesso? E qual é o SLA de entrega (por exemplo, X% das notificações entregues em até Y minutos)? Sem isso, ninguém vai conseguir dizer depois se o projeto funcionou.

3. **Fora de escopo.** Os dois itens só negam os objetivos ("não deve ser lento", "não deve perder notificações") e não excluem nada. O que alguém poderia esperar deste trabalho e vocês decidiram não fazer agora (novos canais, mudança nos templates, preferências do usuário, algo assim)? E "não perder notificações" é na verdade um requisito? Se for, ele pertence aos Objetivos.

4. **O custo aceito.** A seção Solução afirma "mais escalável e robusta, além de mais fácil de manter" e não apresenta nenhum ponto negativo. Solução sem contra é o sinal de alerta número um numa revisão. O que fica pior ou mais caro com o fanout, e o que o time decidiu aceitar em troca? Há algum dado que sustente as afirmações (benchmark, protótipo, carga medida)?

5. **Alternativas.** O documento vai do problema direto para a solução. O que mais foi considerado (paralelizar dentro do serviço atual, encurtar o cron, outra topologia de filas) e por que perdeu? E por que não fazer nada não é aceitável? Isso é o que torna a decisão auditável daqui a um ano.

6. **Lacunas do desenho.** Alguns pontos que o texto e o diagrama deixam em aberto:
   - Qual tecnologia de mensageria? "Exchange" sugere uma, mas o documento não diz.
   - CDC sobre qual fonte e com qual ferramenta? Hoje o cron lê a tabela `notifications`; os "eventos de domínio" vêm dessa mesma tabela ou de outro lugar?
   - Onde vive o controle de TPS por provider (no worker, no dispatcher)? Ele aparece na visão geral mas não no diagrama.
   - O canal in-app não tem DLQ no diagrama. É proposital?
   - O que manda uma mensagem para a DLQ (quantas tentativas, qual política de retry)?

7. **Migração.** Na etapa 2 do plano (e-mail migrado, cron ainda ligado), o que impede cron e worker de enviarem a mesma notificação duas vezes? Há rollback por etapa? E prazos aproximados, mesmo que grosseiros?

8. **Cabeçalho.** O documento está "Em revisão" desde fevereiro. Ainda está? Quem revisa, e de quais áreas? O desenho introduz um componente de mensageria e CDC sobre o banco; quem cuida de infraestrutura e de dados precisa ver isso, e vale nomear essas pessoas como revisores.

Duas sugestões que dependem das respostas acima, não vou aplicar sem elas:

- Com as respostas do item 6, converto o fluxograma num diagrama C4 de containers em Structurizr DSL (imagem renderizada com a fonte dobrada abaixo), que é a convenção que usamos para arquitetura. Sem saber as tecnologias, o diagrama teria caixas vazias e não ajudaria.
- Com as respostas dos itens 4, 5 e 8, cabem seções de "Trade-offs", "Alternativas consideradas" e "Preocupações transversais" (segurança, infraestrutura, carga sobre outros times). Sugiro porque o conteúdo pede, não porque falta um título.

## O que já apliquei

- **Glossário** logo após o cabeçalho, com CDC, DLQ, exchange, fanout, provider, SLA e TPS: o texto usava todos sem definir. A definição de SLA está genérica de propósito; o valor entra quando você responder o item 2.
- **Visão geral** reduzida a um parágrafo sem detalhes (problema e tipo de solução). Os fatos sobre o sistema atual (cron a cada minuto, tabela `notifications`, providers chamados um a um) foram para uma seção nova, **Contexto**, sem alteração de conteúdo. Os detalhes da solução (exchange, DLQ, TPS, CDC) saíram da visão geral e foram para a seção Solução.
- **Texto explicativo após o diagrama**, em quatro etapas (ingestão, roteamento, entrega, falhas), descrevendo só o que o seu texto e o seu diagrama já diziam. As lacunas ficaram nas perguntas, não no documento.
- **Última atualização** ajustada para hoje (2026-09-28).
- O diagrama Mermaid foi mantido como está; validei que renderiza sem erro.

Não mexi em Objetivos, Fora de escopo, na frase de abertura da Solução nem no Plano: todos dependem das suas respostas. Me manda o que conseguir e eu aplico o resto.
