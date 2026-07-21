Dá pra montar o `workspace.dsl`, mas ainda não sem inventar coisa. Olhei o repositório e ele está vazio (nenhum `.dsl`, nenhum diretório de ADRs, nenhum código pra me ancorar), então tudo o que eu não perguntar eu teria que chutar — e arquitetura chutada é pior que lacuna, porque a lacuna alguém pergunta e o chute alguém acredita.

Deixo aqui o que já dá pra classificar com o que você contou, e depois as 4 perguntas que realmente decidem o resto.

## O que já está claro

| Coisa | Classificação C4 | Por quê |
|---|---|---|
| **OrderHub** | Software system — o sistema em escopo do workspace | é o principal, seu time é dono |
| **Pagamentos** (o "negócio de pagamentos" de outro time daqui) | Software system **externo** (caixa fechada, sem containers) | outro time é dono; em C4 você só abre o que o seu time mantém — o time de pagamentos modela o interior dele no workspace *dele* |
| **Redis** | Container (data store) | precisa estar rodando / guarda dados |
| **Job noturno de conciliação de notas fiscais** | Container (processo batch/cron) | ele roda; job agendado é container, não componente |

E o que **não** está decidido: a "plataforma de notificações" pode ser sistema externo ou container de vocês (muda a caixa e o diagrama inteiro), o OrderHub por dentro está vazio (sem isso não existe diagrama de containers), e não sei nenhuma relação com direção/protocolo.

## As perguntas

1. **OrderHub por dentro:** quais aplicações e armazenamentos precisam estar *rodando* pro sistema funcionar — API, front (SPA/app), banco de dados, workers — e com que tecnologia cada um? E quem usa o OrderHub: que pessoas/papéis (cliente final? atendente? operação?)? Os "clientes" que recebem email/push também usam o OrderHub direto, ou só recebem as notificações?

2. **Plataforma de notificações:** quem mantém? Três respostas bem diferentes — (a) seu time, dentro do OrderHub → vira container; (b) outro time daqui → software system externo, igual pagamentos; (c) SaaS de terceiro (SendGrid, Firebase, OneSignal…) → software system externo, e me diz qual. E o OrderHub chama ela como: HTTP síncrono, ou publicando evento numa fila/tópico?

3. **Job de conciliação de notas fiscais:** é do seu time e faz parte do OrderHub (mesmo repo/deploy), ou é um sistema/serviço separado? E ele lê e escreve o quê — banco do OrderHub, o sistema de pagamentos, algum ERP/SEFAZ/arquivo de terceiro?

4. **Redis:** quem lê e quem escreve nele, e pra quê — cache, fila de jobs, sessão, lock? É exclusivo do OrderHub ou compartilhado com outros sistemas? (Se for usado como fila, eu modelo as filas/tópicos, não a "caixa Redis".)

## O que eu faço assim que você responder

- **System Context** e **Container** views (o par recomendado pelo C4) — sempre.
- **Deployment view** só se você quiser: aí preciso saber quais ambientes existem e o que roda onde (cloud, orquestrador, réplicas, gateway/load balancer).
- **Dynamic view** só se tiver um fluxo específico que valha a pena contar passo a passo (ex.: "pedido pago → notificação"), e ele tem que usar relações que já existam no modelo.
- Nada de `!adrs` por enquanto: não achei diretório de ADRs no repo. Se vocês mantiverem um decision log em outro lugar (`doc/adr`, `docs/decisions`), me aponta que eu ligo no workspace.

Depois de escrever eu valido o DSL no servidor MCP do Structurizr que está conectado nesta sessão, e te passo o comando pra abrir o preview em `http://localhost:8080`. Ainda não escrevi nem validei nenhum arquivo.
