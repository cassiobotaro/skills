Antes de escrever o design doc, preciso de algumas respostas suas. Migrar um monólito para microsserviços é uma decisão cara e arriscada, e o valor de um design doc está justamente em registrar os *trade-offs* reais — o que melhora e o que piora — e o *porquê* dessa escolha em vez das alternativas. Eu não consigo inventar esses dados com honestidade: o repositório está vazio, então não tenho como inferir a arquitetura atual nem o que está doendo hoje. Se eu chutasse métricas, restrições e razões, o documento viraria ficção, e quem o lesse depois tomaria decisões com base em coisas que ninguém de fato afirmou.

Por isso, ainda não criei o arquivo. Com as respostas abaixo eu escrevo o documento de verdade. Não precisa responder tudo com precisão cirúrgica — o que você souber já ajuda; o que não souber, registro como questão em aberto.

**1. O problema (o que dói hoje?)**
O que motiva a migração *agora*? Exemplos do tipo de coisa que ajuda: deploys demorados ou arriscados, um time grande pisando no pé do outro, um módulo que não escala junto com o resto, tempo de build, dificuldade de adotar tecnologias diferentes por parte. Sem um problema concreto, "do nothing" (não migrar) pode ser a melhor opção — e o doc precisa conseguir refutar isso.

**2. Como vão saber que deu certo? (de preferência com número)**
Qual é o objetivo mensurável? Por exemplo: "reduzir o tempo de deploy de X para Y", "permitir que os times A, B e C façam deploy de forma independente", "isolar a falha do módulo de pagamentos do resto". E o que está *fora* de escopo desta migração (algo que alguém razoavelmente esperaria, mas que vocês não vão atacar agora)?

**3. O que existe hoje?**
Qual é a stack do monólito (linguagem/framework, banco de dados, como é deployado)? Há algum diagrama, repositório ou doc que eu possa olhar? Qual a ordem de grandeza (tamanho do time, volume de tráfego, nº de módulos)? Isso define o ponto de partida do diagrama de arquitetura.

**4. Já têm uma estratégia de migração em mente?**
Por exemplo: Strangler Fig (extrair um serviço de cada vez por trás de um roteador), big bang (reescrita completa), ou extrair só um ou dois serviços e parar por aí? Qual o primeiro serviço/módulo que pretendem extrair, e qual decisão dessa estratégia vocês têm *menos* certeza? Como ficam os dados — banco compartilhado no começo, ou um banco por serviço desde o início?

**5. Quem é afetado fora do time?**
A migração impacta segurança, infraestrutura/plataforma, ou outros times que consomem APIs do monólito? Quem deveria revisar este documento (e de quais áreas)? E quem são os autores?

Detalhes operacionais menores (autoria, autores, plano de rollout, observabilidade) eu consigo deixar como seções a preencher ou questões em aberto — não preciso disso para começar.

Sobre onde salvar: como o repositório ainda não tem uma convenção, sugiro `docs/design/migracao-monolito-microsservicos.md`. Se preferir outro caminho, me avise.
