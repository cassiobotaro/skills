Posso escrever, mas ainda não tenho o que colocar dentro do documento. "Migrar o monolito para microserviços" é o título de um design doc, não o conteúdo dele — o valor está no problema concreto, nos trade-offs e nas alternativas que vocês já pesaram. Se eu escrever agora, vou inventar métricas, riscos e motivações que ninguém no time falou, e o doc não vai sobreviver à primeira revisão.

Olhei o repositório e ele está vazio: não há design docs anteriores nem template de casa para eu seguir. Então preciso de você em cinco pontos.

**1. Qual é a dor concreta hoje?**
O que especificamente dói no monolito atual — deploys que travam entre times, um módulo que não escala junto com o resto, tempo de build, acoplamento com o banco, incidente que derrubou tudo junto? E por que resolver isso *agora*, e não no semestre passado? (Se puder, me diga também o que é o monolito hoje: linguagem, tamanho aproximado do time, o que ele faz.)

**2. Como vocês vão saber que deu certo?**
De preferência com número: "cada time consegue deployar sem coordenar com os outros", "o módulo X aguenta 3× o pico atual", "reduzir o tempo de build de 40 para 10 minutos". E o inverso: o que está explicitamente **fora** de escopo nesta rodada — o monolito inteiro vai ser fatiado, ou vocês vão extrair um ou dois serviços primeiro e o resto fica onde está?

**3. Que desenho vocês já têm na cabeça?**
Quais serviços sairiam primeiro e por qual critério de corte (domínio, time dono, ponto de gargalo)? Como eles se comunicariam (HTTP síncrono, fila, eventos)? E o banco — cada serviço com o seu, ou continua um banco compartilhado por enquanto? Se ainda não há desenho, me diga isso também: aí a decisão de corte vira a pergunta central do doc.

**4. Qual custo o time já aceitou pagar?**
Essa é a pergunta que dá valor ao documento a longo prazo, e ela não sai sozinha da pergunta anterior. Microserviços cobram em latência de rede, consistência eventual, observabilidade distribuída, mais pipelines e mais on-call. O que vocês já decidiram engolir, e o que ainda está em aberto?

**5. Quem é impactado fora do time, e o que mais foi considerado?**
Infra/plataforma, segurança, times que consomem APIs do monolito, dados? E: além de "migrar para microserviços", o que mais entrou na mesa — modularizar o monolito sem quebrá-lo, extrair só o gargalo, ou simplesmente **não fazer nada**? Preciso saber por que não fazer nada foi descartado; se não houver resposta boa para isso, o problema ainda não está maduro para um doc.

Responda o que souber — nem tudo precisa vir de uma vez, e "ainda não sabemos" é uma resposta válida (vira a seção de questões em aberto). Com os pontos 1, 2 e 4 respondidos eu já consigo escrever um primeiro rascunho honesto e marcar o resto como aberto.

Duas coisas menores, para eu já deixar o arquivo no lugar certo: onde vocês guardam design docs (sugiro `docs/design/`), e quem assina como autor e quais áreas devem revisar (segurança, plataforma, os times donos dos módulos que saem primeiro).
