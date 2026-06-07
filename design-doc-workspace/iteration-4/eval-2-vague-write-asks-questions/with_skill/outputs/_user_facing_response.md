Posso escrever esse design doc, mas migrar um monolito para microsserviços é uma decisão cheia de trade-offs, e um doc que pula direto do problema para a solução perde todo o valor. Para que o documento registre o *seu* raciocínio (e não um genérico que eu inventaria), preciso de algumas respostas antes de escrever. Não vou preencher nada com suposições.

Quatro a cinco perguntas, da mais importante para a menos:

1. **Qual é a dor de hoje?** O que especificamente está doendo no monolito que motiva isso agora — deploys que travam o time todo, dificuldade de escalar uma parte específica, áreas do código que ninguém mexe sem medo, acoplamento entre times? Quanto mais concreto (e com número, se houver — ex.: "deploy leva 40 min e bloqueia 5 times"), melhor.

2. **Como vocês vão saber que deu certo?** Existe alguma meta mensurável — reduzir tempo de deploy de X para Y, permitir que cada time entregue de forma independente, escalar o módulo Z separadamente? E o que está explicitamente *fora* de escopo nessa primeira rodada (ex.: "o módulo de billing continua no monolito por enquanto")?

3. **Qual é a forma da solução que vocês já têm em mente?** Vocês pensam em extrair tudo de uma vez ou ir aos poucos (ex.: strangler fig, extraindo um serviço por vez)? Já têm ideia de quais capacidades viram os primeiros serviços e por onde começar? E qual decisão dessa migração é a que vocês estão *menos* seguros?

4. **O que mais foi considerado — e por que "não fazer nada" não serve?** Houve alternativas na mesa (modularizar o monolito sem dividir em serviços, um monólito modular, só extrair o que está em chamas)? E por que continuar como está hoje não é aceitável? (Todo design doc precisa registrar o custo aceito: o que piora — complexidade operacional, latência de rede, consistência distribuída, custo de infra — em troca do que melhora.)

5. **Quem é impactado fora do time que vai fazer a migração?** Isso muda contratos de API que outros times consomem, adiciona carga a sistemas compartilhados (banco, fila, gateway), abre novas superfícies de segurança, ou depende de infra/plataforma que outro time controla? Quem deveria revisar (Segurança, Plataforma, Infra)?

Bônus, se já estiver decidido: quem são os autores e quais áreas/times devem revisar o doc — assim eu já preencho o cabeçalho.

Me responda o que conseguir (mesmo que parcial) e eu escrevo o design doc em Markdown, organizado em torno dos trade-offs, com diagrama de arquitetura (C4 container) e dos fluxos relevantes. O que você não souber ainda, eu registro como "questões em aberto" em vez de inventar.
