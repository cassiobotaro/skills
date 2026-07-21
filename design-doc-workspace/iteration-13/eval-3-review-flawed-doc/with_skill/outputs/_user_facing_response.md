Revisei o `docs/design/fanout-de-notificacoes.md`. O achado mais importante é que o
documento não tem trade-offs nem alternativas: ele vai do problema direto para a solução
e a apresenta como "mais escalável, robusta e fácil de manter", sem um único custo
aceito. Isso é justamente o que dá valor ao doc daqui a um ano, e só você pode preencher
— está na lista de perguntas. Já apliquei o que não dependia de você.

## Perguntas para você

1. **Existe um template de design doc que a casa segue?** (wiki, drive, outro repo).
   Templates normalmente moram fora do repositório, então o que eu encontro aqui é pista,
   não resposta. Enquanto não me disser, estou medindo o documento pelo catálogo padrão
   de seções — ou seja, o que eu sugerir de estrutura é sugestão, não exigência.
2. **Qual custo o time aceitou?** O que ficou pior, mais arriscado ou mais caro com o
   fanout? (Mais peças para operar? Perda de ordem entre canais? Entrega duplicada?
   Custo de infraestrutura do broker?) Sem pelo menos um custo explícito, a seção de
   solução continua lendo como venda.
3. **O que mais vocês consideraram, e por que perdeu?** Inclusive o "não fazer nada":
   por que continuar com o cron sequencial não é aceitável?
4. **Os objetivos precisam de número.** Qual é o SLA de entrega (p. ex. "95% em até 30s")
   e qual é a latência hoje? "Melhorar a performance" e "tornar escalável" não são
   verificáveis — escalável em relação a qual volume?
5. **O que fica de fora de propósito?** Os dois itens que estavam em "Fora de escopo"
   eram negação dos objetivos e não excluíam nada. Algo que alguém poderia razoavelmente
   esperar deste trabalho e que vocês *não* vão fazer? (Ex.: preferências de canal por
   usuário, novos canais, reprocessamento automático da DLQ.)
6. **Quem é impactado fora do time?** O broker é compartilhado com outros times? O CDC
   adiciona carga na base de mensageria? Os providers têm limite contratado de TPS?
   Vale uma seção de preocupações transversais e revisores dessas áreas no cabeçalho.
7. **Tecnologias não estabelecidas.** O texto não diz qual broker, qual ferramenta de CDC
   nem qual base guarda a tabela `notifications` — deixei essas caixas do diagrama sem
   tecnologia de propósito, para não decidir por você. Me diga e eu preencho.
8. **Cabeçalho:** o estado ainda é "Em revisão" desde fevereiro? E quem são os revisores
   (com a área de cada um)?
9. **Como vocês verificam e observam isso?** O que prova antes de subir e qual métrica/
   alerta mostra em produção que o fanout está entregando dentro do SLA. E o plano de
   entrega tem rollback se uma etapa der errado?
10. **Ficou alguma questão em aberto** (dono do CDC, política de retentativa e de
    esvaziamento das DLQs)? Vale registrar em vez de esconder.

## O que já apliquei

- **Visão geral enxugada** para dois parágrafos sem detalhes; toda a descrição do
  funcionamento atual (cron de um minuto, tabela `notifications`, envio sequencial)
  virou uma seção **Escopo e contexto**, que é onde o leitor precisa dela.
- **Removi a frase de venda** ("mais escalável e robusta que o modelo atual, além de mais
  fácil de manter") e escrevi a solução descrevendo o que cada peça faz. Ela volta como
  afirmação assim que houver o dado que a sustente — e o contraponto (pergunta 2).
- **Glossário no início do documento**, cobrindo os termos que o texto usa sem explicar:
  CDC, DLQ, TPS, SLA, exchange, fanout, push e in-app.
- **Diagrama de arquitetura refeito** como diagrama de containers C4 em Structurizr DSL,
  validado, renderizado em `docs/design/diagrams/fanout-de-notificacoes-containers.svg` e
  embutido como imagem com a fonte dobrada logo abaixo. O flowchart anterior também
  estava incompleto: faltava a **DLQ do canal in-app** (o texto diz "DLQ por canal") e os
  providers, que agora aparecem. Nenhuma tecnologia foi inventada nas caixas.
- **Texto explicativo depois do diagrama**, nomeando cada componente e como eles
  interagem — antes o diagrama estava sozinho.
- **"Não perder notificações" virou objetivo** (estava listado como fora de escopo) e o
  "não deve ser lento" saiu por repetir o objetivo de performance. A seção Fora de escopo
  ficou com uma nota do que aconteceu, à espera da sua resposta na pergunta 5.
- **Última atualização** do cabeçalho ajustada para 2026-07-21.

Assim que você responder as perguntas, eu escrevo as seções de trade-offs, alternativas
consideradas, preocupações transversais e observabilidade com o que você me disser.
