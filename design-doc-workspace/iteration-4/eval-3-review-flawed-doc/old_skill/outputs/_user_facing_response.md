Revisei o `docs/design/fanout-de-notificacoes.md`. Apliquei direto as melhorias que não dependiam de você e deixei marcado, no próprio doc e abaixo, o que precisa da sua resposta. Mantive o português, a estrutura e a voz do documento — só ajustei e completei.

## Melhorias já aplicadas

- **Glossário** (logo após o cabeçalho): o doc se apoia em vários termos que um revisor de outro time tropeçaria — defini *fanout*, **CDC**, **DLQ**, **TPS**, **SLA** e *provider*.
- **Visão geral enxugada**: ela estava cheia de detalhe técnico (CDC, exchange, TPS, DLQ) que é trabalho das seções seguintes. Reescrevi em linguagem simples (qual o problema e que tipo de solução), sem inventar nada.
- **Nova seção "Escopo e contexto"**: movi para cá os fatos do "como funciona hoje" (cron a cada minuto, leitura da tabela `notifications`, chamada serial aos providers) que estavam misturados na visão geral. É o mesmo conteúdo que você já tinha escrito, só reposicionado.
- **Texto explicativo após o diagrama**: o diagrama estava sozinho. Acrescentei um parágrafo descrevendo cada componente (CDC → dispatcher → exchange → filas por canal → workers → DLQ) e por que o processamento deixa de ser serial. Tudo derivado do próprio diagrama e da sua visão geral.
- **Correção de consistência no diagrama**: o diagrama tinha DLQ só para push e e-mail, mas o texto diz "DLQ por canal". Adicionei a `DLQ in-app` para o diagrama bater com o que você descreveu. (Observação: o servidor de validação de Mermaid estava com erro no momento, então essa alteração não foi validada por máquina — é uma adição trivial, idêntica ao padrão das outras DLQs.)
- **"Plano" → "Plano de implantação"** e **cabeçalho**: marquei `Última atualização` como 2026-06-07 (data real da revisão) e adicionei a linha **Revisores** com `(a definir)`.
- **Notas de revisão inline**: marquei dentro do doc, com uma citação curta, os três pontos que mais enfraquecem o documento hoje (objetivos não mensuráveis, fora-de-escopo que só nega os objetivos, e a solução sem custos/alternativas) para você não perdê-los de vista — elas saem assim que você responder as questões abaixo.

## Questões para você (precisam da sua informação — não dá pra inventar)

Essas são lacunas de conteúdo que só você consegue preencher. São o que mais agrega valor ao doc:

1. **Trade-offs da solução (o mais importante):** a seção "Solução" hoje só lista vantagens ("mais escalável e robusta, mais fácil de manter"). Qual custo o time aceitou em troca? Por exemplo: operar fila + DLQ + CDC é mais complexo que um cron; passa a haver entrega assíncrona/eventual; mais peças para monitorar. O que ficou pior, mais arriscado ou mais caro?

2. **Alternativas consideradas + "não fazer nada":** o que mais foi avaliado antes de escolher o fanout com filas (ex.: paralelizar o cron com threads/pool, usar um scheduler dedicado, um SaaS de notificações)? E por que continuar como está (o "não fazer nada") não é aceitável?

3. **Objetivos mensuráveis:** "melhorar a performance", "tornar escalável" e "garantir o SLA" não são verificáveis. Tem números? Por exemplo: "reduzir a latência p95 de envio de X para Y", "sustentar Z envios/min", "qual é o SLA exato (prazo de entrega) e qual a meta de cumprimento (ex.: 99,5%)"?

4. **Fora de escopo real:** o que alguém poderia razoavelmente esperar desta entrega mas está deliberadamente de fora? (ex.: "novos canais como SMS/WhatsApp ficam fora", "priorização/agendamento de notificações fica para depois", "deduplicação não muda nesta fase".)

5. **Revisores:** quais áreas/times deveriam revisar? O CDC mexe no banco/time de dados; os providers e a fila tocam infra; os payloads de notificação podem conter dados pessoais (segurança). Quem nomear como revisor de cada área?

6. **Concerns transversais (vale uma seção):** (a) o CDC adiciona carga/risco ao banco de domínio — o time de dados está ciente? (b) os payloads têm PII? (c) a fila/exchange é infra nova ou compartilhada? Posso criar a seção quando você me passar os detalhes.

7. **Testabilidade/observabilidade e rollback:** como você vai validar antes de subir e o que vai te dizer que está funcionando (ou quebrado) em produção? E no plano de implantação — se a migração de um canal der errado, qual é a volta atrás? Hoje não há essa história.

8. **Estado do documento:** está "Em revisão" desde 10/02. Ele deve avançar de estado (ex.: para "proposto"/"aprovado") ou continua em revisão?

Me responda o que quiser dessas e eu incorporo direto no documento (as notas de revisão inline saem junto).
