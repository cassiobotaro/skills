Revisei o `docs/design/fanout-de-notificacoes.md`. Não achei outros design docs no
repositório, então não existe um template da casa que eu possa usar como régua — segui o
catálogo padrão de seções, e por isso as sugestões estruturais abaixo são sugestões, não
exigências (a primeira pergunta da lista é justamente sobre isso).

## O que já apliquei

1. **Visão geral enxugada e contexto separado.** A visão geral tinha o documento inteiro
   dentro dela: arquitetura atual, solução proposta, CDC, DLQ, TPS e SLA num parágrafo
   só. Reduzi para duas frases ("o que é isso e o que entrega") e movi os fatos do modelo
   atual (cron de um minuto, tabela `notifications`, chamada sequencial aos providers)
   para uma seção nova **Escopo e contexto**, que é onde o leitor se situa antes de ver a
   proposta.
2. **Glossário no começo do documento.** O texto se apoia em CDC, DLQ, TPS, SLA, fanout,
   exchange, worker, provider e in-app sem definir nenhum — qualquer revisor de fora do
   time de mensageria tropeça já na visão geral. Adicionei o glossário logo depois do
   cabeçalho, com uma linha por termo.
3. **Tirei o discurso de venda da seção Solução.** "Mais escalável e robusta que o modelo
   atual, além de mais fácil de manter" são três afirmações sem nenhum dado por trás, e
   é exatamente o tipo de frase que um revisor devolve com "por quê?". Troquei por uma
   descrição factual do mecanismo (quem publica, quem consome, o que é paralelo). As
   qualidades voltam ao documento no dia em que virarem trade-offs com número — veja a
   pergunta 3.
4. **Diagrama de arquitetura como diagrama de container C4.** O `flowchart` do Mermaid não
   dizia o que cada caixa é nem o que corre em cada seta. Reescrevi o modelo em
   Structurizr DSL, validei com o servidor MCP do Structurizr (sem erros), renderizei em
   SVG e embuti a imagem em `docs/design/diagrams/arquitetura-fanout.svg`, com a DSL
   dobrada num `<details>` logo abaixo — a DSL é a fonte da verdade, a imagem é o que o
   leitor vê. Mantive exatamente os elementos e ligações que você tinha desenhado; só
   acrescentei os providers como sistema externo, porque o próprio texto já falava deles.
5. **Texto explicando o diagrama.** Não havia nenhuma prosa depois da figura: o leitor
   via caixas e tinha que adivinhar o significado. Escrevi um parágrafo nomeando cada
   componente e dizendo como eles interagem — em especial onde nasce o paralelismo (uma
   fila e um worker por canal) e o papel da DLQ.
6. **Cabeçalho.** Atualizei a *Última atualização* para 2026-07-20, já que o documento
   mudou hoje.

## O que precisa de você

1. **Existe um template de design doc no time?** Templates normalmente moram no wiki ou
   no drive, não no repositório — o que eu vejo aqui é pista, não resposta. Se existir,
   me passa a referência que eu remeço o documento contra ele; se não existir, as
   sugestões estruturais abaixo continuam sendo sugestões.
2. **Os objetivos não são verificáveis.** "Melhorar a performance", "tornar o sistema
   escalável" e "garantir o SLA" não dão para checar depois: como você vai saber que deu
   certo? Qual é o SLA em número (p. ex. "95% das notificações entregues em até 60s")? De
   quanto é a lentidão hoje e para onde ela precisa ir? E "escalável" até que volume —
   qual é o pico esperado da base? Deixei os objetivos como estavam; me manda os números
   e eu reescrevo.
3. **Fora de escopo não exclui nada.** "O sistema não deve ser lento" e "não deve perder
   notificações" são requisitos, não exclusões — são a negação dos objetivos. O que
   alguém razoavelmente esperaria deste trabalho e que ele *não* vai cobrir? Alguns
   candidatos que costumam aparecer: notificação por SMS/WhatsApp, agendamento de envio,
   preferências de opt-out por canal, reprocessamento automático da DLQ, migração do
   histórico antigo.
4. **Falta a seção de trade-offs — é a lacuna mais grave do documento.** Hoje a solução
   aparece sem um único custo, e uma solução sem custo é propaganda. O fanout traz
   consistência eventual, ordenação por canal, risco de entrega duplicada, um broker novo
   para operar e monitorar, DLQs para alguém drenar e um caminho de depuração bem mais
   difícil que "ler a tabela". Qual desses custos vocês aceitaram conscientemente, e tem
   algum outro? Um `✓`/`✗` já resolve.
5. **Faltam as alternativas consideradas — inclusive "não fazer nada".** O que mais foi
   avaliado antes de escolher o fanout com filas? Manter o cron e só paralelizar com
   threads/processos? Aumentar a frequência do cron? Usar o broker sem CDC, publicando
   direto do serviço? Um serviço de notificação de terceiro? E por que continuar como
   está não é aceitável — o que quebra se não fizermos nada este trimestre?
6. **Quem é impactado fora do time?** O CDC e o broker normalmente envolvem
   infraestrutura; os providers impõem limites de TPS que alguém negocia; a base de onde
   o CDC lê pertence a alguém. Que times precisam revisar isso (infra, segurança, donos
   dos eventos de domínio)? Vale nomeá-los como revisores no cabeçalho — hoje o autor é
   "Time de Mensageria" e não há nenhum revisor listado. Quem assina o documento?
7. **Três dúvidas concretas sobre o diagrama**, que eu não quis preencher por conta:
   - O canal **in-app não tem DLQ** no desenho. É intencional (o in-app não falha da mesma
     forma?) ou é um esquecimento?
   - **De qual base o CDC captura** os eventos de domínio, e quais eventos?
   - **Onde mora o controle de TPS** — dentro do worker, num rate limiter compartilhado,
     na configuração de prefetch da fila?
8. **Qual é a tecnologia da exchange, das filas e dos workers?** Deixei os containers sem
   tecnologia na DSL de propósito, para não inventar "RabbitMQ" a partir do vocabulário
   de exchange/DLQ. Me confirma o broker e a linguagem dos workers que eu preencho.
9. **O plano não tem rollback nem critério de avanço.** Os quatro passos estão claros, mas:
   o que faz vocês decidirem que o e-mail migrado está saudável antes de migrar push e
   in-app? Dá para voltar ao cron se a fase 2 der errado (os dois caminhos convivem)? Há
   um prazo aproximado por fase?
10. **O estado ainda é "Em revisão" desde fevereiro.** Se o documento estiver parado ou já
    aprovado, vale atualizar — um doc "em revisão" há cinco meses confunde quem chega
    depois.

Além disso, sugiro duas seções que este documento pediria (não há template governando, então
são sugestões): **Testabilidade e observabilidade** — o fanout troca uma execução síncrona
por filas, e o sinal de que está funcionando deixa de ser óbvio: quais métricas e alertas
provam o SLA (lag da fila, taxa de DLQ, latência por canal)? — e **Perguntas em aberto**,
para registrar o que ainda depende de outros times em vez de deixar implícito.

Me responde o que fizer sentido e eu incorporo direto no documento.
