Revisei o `docs/design/fanout-de-notificacoes.md`. Apliquei o que era só clareza e estrutura, sem mexer no que você decidiu; o que precisa de você está na lista de perguntas no fim. A leitura geral: o documento descreve bem o que vai ser construído, mas ainda não diz por quê esse caminho e não outro, nem o que piora em troca do que melhora. Essa é a parte que só você consegue preencher.

## O que eu já apliquei

1. **Glossário logo após o cabeçalho.** O texto usa CDC, DLQ, TPS, SLA e "provider" sem definir. Um revisor de outro time tropeça em CDC e DLQ na primeira leitura. As definições são genéricas (o que a sigla significa e o papel que ela tem aqui); o número do SLA e a taxa de TPS continuam sendo perguntas suas.
2. **Visão geral enxuta, detalhes movidos para um "Contexto".** A visão geral misturava o estado atual (cron, tabela `notifications`, providers um a um), a solução inteira (exchange, workers, DLQ, TPS, CDC) e a promessa de resultado, tudo em um parágrafo. Agora ela diz o problema e o tipo de solução em duas frases; os fatos do sistema atual ficaram em "Contexto" (só fatos, sem solução) e os componentes da solução foram para "Solução". Nenhuma informação foi perdida, só mudou de lugar. Se preferir manter tudo na visão geral, é só reverter.
3. **Texto explicando o diagrama.** O flowchart estava sozinho; adicionei um parágrafo abaixo dele nomeando cada componente e o que flui entre eles, usando apenas o que o seu texto já dizia (CDC, dispatcher, exchange, uma fila e um worker por canal, controle de TPS por provider, DLQ por canal). Não mexi no diagrama em si, e ele renderiza sem erro no mermaid-cli.
4. **Frase de vendas removida da Solução.** "A solução proposta é mais escalável e robusta que o modelo atual, além de mais fácil de manter" afirma três vantagens sem um fato que as sustente e sem nenhum custo ao lado. Tirei do corpo e transformei em pergunta (item 5 abaixo): quando você me disser o que sustenta cada afirmação e o que piora, isso vira uma seção de trade-offs de verdade.
5. **Cabeçalho: "Última atualização" para 2026-09-28**, a data de hoje, já que o arquivo mudou.
6. Voz ativa e dois pontos de "revelação" retirados do que reescrevi; o restante do texto seu já estava direto.

O que eu **não** mexi porque depende de você: Objetivos, Fora de escopo, Plano e o diagrama. Estão como você escreveu.

## Perguntas para você

Respondendo, eu escrevo as seções correspondentes com o seu conteúdo.

1. **Template.** O time tem um template de design doc (wiki, drive)? Se tiver, me passa a referência, para eu propor as seções nos termos dele e não nos meus.
2. **Cabeçalho.** Quem são os autores (pessoas, não só o time)? Quem deveria revisar, e de qual área (infra do broker, dono do banco de onde o CDC lê, times que emitem os eventos de domínio)? E o estado ainda é "Em revisão"? Ele está assim desde fevereiro; se o doc parou ou já foi aprovado, o cabeçalho deveria dizer.
3. **O problema em números.** "Começou a apresentar lentidão" é a motivação inteira do documento e não tem número. Qual é o atraso hoje entre a notificação entrar na tabela e ser entregue? Qual o volume atual e o esperado? E qual é o SLA de entrega que precisa ser garantido (X minutos para Y% das notificações)?
4. **Objetivos mensuráveis.** Os três objetivos ("melhorar a performance", "tornar escalável", "garantir o SLA") não dão para verificar depois. Para cada um, qual é o número que diz que deu certo? Exemplo do formato, não do conteúdo: "entregar 99% das notificações em até N minutos com o dobro do volume atual".
5. **Trade-offs e evidências.** O que piora com o fanout, e o que o time decidiu aceitar em troca? Mais peças para operar (broker, filas, DLQs, o próprio CDC), atraso do CDC, possibilidade de entrega duplicada, ordem dos eventos, custo de infra? E o que sustenta "mais escalável, mais robusto, mais fácil de manter": houve um protótipo, um benchmark, um número de carga?
6. **Alternativas.** O que mais foi considerado antes do fanout com filas? Em particular, por que não ajustar o modelo atual (paralelizar dentro do serviço, aumentar a frequência ou o lote do cron)? E por que "não fazer nada" não é aceitável, dado o item 3?
7. **Fora de escopo.** Os dois itens de hoje negam os objetivos em vez de excluir algo ("não deve ser lento" é o objetivo 1 de outra forma). O que alguém poderia esperar que este trabalho cobrisse e não vai cobrir (novos canais, templates, preferências do usuário, retentativa automática da DLQ, qualquer outra coisa)? E "não perder notificações" me parece um requisito, não uma exclusão: se for, eu movo para os objetivos, e aí preciso saber qual garantia você espera (pelo menos uma vez? e o que acontece com o que cai na DLQ?).
8. **Consistência do diagrama.** Três pontos onde o texto e o desenho divergem ou deixam um vazio:
   - O texto diz "DLQ por canal", mas o diagrama tem DLQ só para push e e-mail. In-app não tem DLQ de propósito?
   - Os providers e o controle de TPS aparecem no texto, mas não no diagrama. Cada canal tem um provider externo, inclusive in-app?
   - De onde o CDC lê: da tabela `notifications` que o cron lê hoje, ou dos bancos dos domínios que emitem os eventos? E cada evento vai para todas as filas ou é roteado por canal?
   - Qual é o broker (você usa "exchange", que sugere um específico, mas o doc não nomeia) e o fanout roda dentro do serviço de mensageria ou vira um serviço novo?
   Com essas respostas eu converto o diagrama para o formato C4 de containers que este skill usa (Structurizr DSL, com a imagem renderizada e o fonte dobrado abaixo). Não fiz agora porque a conversão obrigaria a decidir por você exatamente esses pontos.
9. **Quem fora do time é impactado.** O design coloca um broker novo, liga um CDC num banco de alguém e passa a bater nos providers com uma taxa controlada. Quem precisa olhar isso: infra, o dono do banco, os times de domínio, alguém que negocia limite com os providers?
10. **Plano.** Por que e-mail migra primeiro? Enquanto o cron ainda roda e a fila de e-mail já está ativa, como se evita envio duplicado? Há como voltar atrás em cada etapa se algo der errado? E como vocês vão saber, em produção, que o SLA está sendo cumprido (métrica, alerta)?

## Seções que o conteúdo pede

Não são obrigatórias; sugiro porque o texto atual as pede. Estou usando os nomes do catálogo padrão até você me dizer se existe um template da casa.

- **Trade-offs da solução escolhida**: a Solução hoje só tem lado bom (era a frase que removi). Com o item 5 respondido, vira uma lista de "ganha isso, custa aquilo".
- **Alternativas consideradas**: o doc vai do problema direto à solução; item 6.
- **Preocupações transversais**: o design toca broker, banco e providers, e nada dá aos times afetados um lugar para revisar; item 9.
- **Questões em aberto**: o que dos itens acima ficar sem resposta agora pode ser registrado ali honestamente, em vez de ficar implícito.

Me manda as respostas que você tiver, mesmo parciais, e eu aplico o resto.
