Revisei o `docs/design/fanout-de-notificacoes.md`. O documento descreve bem *o que* vai ser construído, mas hoje ele não registra *por que* essa solução venceu nem o que ela custa — é aí que está a maior parte das perguntas abaixo. Já apliquei no arquivo tudo o que não depende de você.

## Perguntas para você (o que eu não posso preencher sem inventar)

1. **Existe um template de design doc no time?** Não achei outro design doc no repositório para servir de referência, e template costuma morar em wiki/drive, não no repo. Se houver, me passa que eu remedo o documento nas seções dele — até lá revisei contra o catálogo padrão, então as sugestões de estrutura são sugestões, não exigências.
2. **Quais são os trade-offs da solução?** Hoje não há uma linha sobre custo: fanout com filas troca latência baixa e isolamento por canal por mais peças para operar, entrega assíncrona e complexidade de reprocessamento. O que *piorou* na sua avaliação, e o que o time decidiu conviver? Uma solução sem contras é o sinal de alerta clássico de um design doc.
3. **Quais alternativas foram consideradas e por que perderam?** Por exemplo: paralelizar o cron atual com threads/processos, usar um scheduler externo, terceirizar o fanout no próprio provider — e, obrigatoriamente, **não fazer nada**. Por que continuar com o cron é inaceitável?
4. **Os objetivos precisam de número.** "Melhorar a performance", "tornar escalável" e "garantir o SLA" não são verificáveis. Qual é a latência/vazão de hoje e a meta (ex.: "p95 de entrega abaixo de 30s com 10x o volume atual")? E qual é exatamente o SLA de entrega acordado?
5. **O "Fora de escopo" hoje só nega os objetivos.** "Não deve ser lento" e "não deve perder notificações" são requisitos, não exclusões — e "não perder notificações" provavelmente deveria virar objetivo. O que alguém razoavelmente esperaria deste trabalho e que ele *não* vai cobrir? (Ex.: novos canais como SMS/WhatsApp, agendamento de envio, deduplicação, preferências de notificação.)
6. **DLQ por canal ou só em dois canais?** A visão geral diz "DLQ por canal", mas o diagrama original só tinha DLQ de push e de e-mail. Mantive as duas que estavam desenhadas. O in-app tem DLQ? E qual é a política de reprocessamento/retry antes de mandar para a DLQ?
7. **Quem é impactado fora do time?** Vale uma seção de temas transversais: infraestrutura (broker novo? o CDC lê a réplica ou o primário?), segurança (payload de notificação carrega dado pessoal?), e os donos do banco `notifications` — o CDC impõe carga neles.
8. **Como isso vai ser verificado e observado?** O que prova que funcionou antes de subir (teste de carga? shadow?) e quais métricas/alertas mostram em produção (idade da fila, tamanho da DLQ, taxa de erro por provider)?
9. **O plano tem rollback?** Nos passos 2 e 3, se a migração de um canal der errado, dá para voltar ao cron sem perder ou duplicar envio? Há período de operação em paralelo?
10. **Cabeçalho:** o doc está "Em revisão" desde fevereiro — o estado ainda é esse? E quem são os revisores nomeados, com área (mensageria, infra, segurança)? "Time de Mensageria" como autor funciona, mas revisor sem nome ninguém cobra.
11. **Questões em aberto:** tem algo ainda indefinido (escolha do broker, dono do CDC, ordenação de eventos) que valha registrar numa seção própria?

## O que eu já apliquei

- **Glossário no início do documento.** O texto se apoia em fanout, exchange, CDC, DLQ, TPS, SLA e in-app sem definir nenhum — agora cada termo tem uma linha, logo depois do cabeçalho.
- **Visão geral enxugada e contexto separado.** A visão geral tinha um parágrafo único com toda a arquitetura dentro (cron, tabela, DLQ, TPS, CDC). Ela agora diz em duas frases qual é o problema e que tipo de solução se propõe; os fatos do sistema atual foram para uma seção **Escopo e contexto**.
- **Removi os adjetivos sem lastro da Solução.** "Mais escalável e robusta que o modelo atual, além de mais fácil de manter" não sobrevive a um "por quê?" de revisor — troquei por uma descrição direta do que a solução faz. Quando você responder a pergunta 2, isso vira uma seção de trade-offs de verdade.
- **Diagrama de arquitetura reescrito como C4 (Structurizr DSL) e renderizado.** O `flowchart` do Mermaid virou um diagrama de containers: cada caixa declara o que é (fila, banco, worker) e cada seta diz o que trafega. O SVG está em `docs/design/diagrams/arquitetura-fanout.svg`, com o DSL dobrado num `<details>` logo abaixo. Aproveitei para incluir o que o texto citava e o desenho não mostrava: a tabela `notifications`, os providers externos e o usuário.
- **Texto explicando o diagrama.** O diagrama antigo aparecia sem uma linha de explicação. Agora ele é seguido de dois parágrafos nomeando os componentes e o caminho do evento — incluindo o ponto que justifica o desenho: cada canal tem fila e worker próprios, então um provider lento segura só a fila dele.
- **Data de última atualização** ajustada para 2026-07-21.

## Sugestões que dependem das suas respostas

Depois que você responder, eu acrescento: **Trade-offs da solução**, **Alternativas consideradas** (com o "não fazer nada"), **Temas transversais**, **Testabilidade e observabilidade** e **Questões em aberto** — e reescrevo Objetivos e Fora de escopo com números e exclusões reais. Um diagrama de sequência do caminho de um envio (incluindo a falha que leva à DLQ) também ajudaria, mas só depois que a política de retry estiver definida.
