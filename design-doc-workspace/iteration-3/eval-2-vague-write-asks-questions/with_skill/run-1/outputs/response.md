Boa! Migração de monolito pra microserviços é exatamente o tipo de decisão onde um design doc vale ouro — mas só se ele registrar **o seu raciocínio**: o que dói hoje, os trade-offs que vocês estão aceitando e as alternativas que descartaram. Esse é o coração do documento, e é justamente o que eu não posso inventar.

O repositório aqui está vazio (sem código, sem docs de design existentes pra eu me basear), e o pedido tá bem aberto. Então, antes de escrever, preciso te fazer algumas perguntas. Não é burocracia: é onde nasce o valor do doc. Quanto mais concreto você for, mais útil ele fica.

## O que eu preciso saber

**1. O problema — por que migrar, e por que agora?**
Qual é a dor concreta do monolito hoje? Por exemplo: deploys lentos ou arriscados, um time travando o outro, um módulo que precisa escalar sozinho mas arrasta o resto, build/CI demorado, dificuldade de contratar/onboarding... Se der, traga números (tempo de deploy, frequência de incidentes, tamanho do time). "Microserviços" é a solução proposta — eu preciso entender o problema que ela resolve, senão o doc vira manual sem o "porquê".

**2. As fronteiras — como vocês vão saber que deu certo, e o que está fora?**
Tem alguma meta mensurável (ex.: "reduzir o tempo de deploy de 2h pra 10min", "permitir que o time de pagamentos faça deploy sem coordenar com os outros 4 times")? E o que explicitamente **não** entra nesta migração (ex.: "o módulo de relatórios continua no monolito por enquanto")?

**3. A solução — vocês já têm um recorte em mente?**
Vão quebrar tudo de uma vez ou extrair serviço por serviço (ex.: strangler fig)? Já existe um candidato a primeiro serviço a ser extraído? Como imaginam comunicação entre serviços (REST síncrono, mensageria/eventos), e o que acontece com o banco de dados (continua compartilhado, um por serviço)? Stack atual do monolito (linguagem, framework, banco) também ajuda.

**4. As alternativas — o que mais foi considerado?**
Microserviços não é a única saída. Vocês chegaram a pensar em: modularizar o monolito sem quebrá-lo (modular monolith), extrair só 1–2 serviços críticos em vez de tudo, ou simplesmente **não fazer nada** e conviver com a dor? Saber por que essas opções perderam é o que torna a decisão auditável depois.

**5. O raio de impacto — quem é afetado além do seu time?**
A migração mexe com infraestrutura (Kubernetes, service mesh, observabilidade distribuída)? Segurança (novas superfícies de rede entre serviços, autenticação serviço-a-serviço)? Outros times que consomem APIs do monolito hoje? Quantos times vão tocar nisso?

## Coisas práticas pra eu já deixar encaminhado

- **Onde salvar o doc?** Sugiro `docs/design/` (ex.: `docs/design/migracao-monolito-microservicos.md`), mas me diz se vocês têm outro lugar.
- **Quem assina e quem revisa?** Quem são os autores e quais áreas/times deveriam revisar (Infra, Segurança, os times impactados)?

---

Se você responder pelo menos as perguntas **1, 2 e 4** (problema, metas e alternativas), já consigo escrever um rascunho sólido e a gente refina o resto junto. Se preferir, me joga o que você tiver em texto livre — bullets, conversa de corredor, o que for — que eu organizo no formato de design doc, sempre mantendo só o que você de fato me passar (não vou preencher buracos com suposições).

Por enquanto não criei nenhum arquivo, justamente pra não gerar um doc cheio de placeholders inventados. Assim que você me der a substância, eu escrevo.
