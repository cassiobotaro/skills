Antes de escrever, preciso do teu raciocínio: um design doc de migração vale pelos trade-offs e pelas alternativas que o time considerou, e nada disso dá pra inventar. Olhei o repositório e ele está vazio — não há código nem design docs anteriores, então também não consigo deduzir a arquitetura atual nem um template da casa.

Me responde estas perguntas (pode ser em tópicos curtos) que eu escrevo o documento em seguida:

1. **Problema e motivação** — o que dói hoje no monolito, e por que resolver agora? (deploys travados, um módulo que não escala, time crescendo, incidentes recorrentes…) Qual é a stack atual e o tamanho aproximado do sistema?

2. **Objetivos e fora de escopo** — como vocês vão saber que a migração deu certo? Se houver número, melhor ("reduzir o tempo de deploy de 2h para 15min", "isolar o serviço de pagamentos para escalar sozinho"). E o que vocês explicitamente *não* vão resolver desta vez (banco único, autenticação, front-end, extração de todos os módulos)?

3. **A solução pretendida** — quais serviços vocês pretendem extrair primeiro e por qual critério? Como eles vão se comunicar (HTTP síncrono, mensageria) e o que acontece com o banco de dados — cada serviço com o seu, ou banco compartilhado por um tempo? Qual decisão desse desenho vocês têm menos certeza?

4. **Custo aceito** — o que essa migração piora? Migração para microserviços costuma cobrar em latência, complexidade operacional, consistência eventual, custo de infra e debugging distribuído. Qual desses o time olhou e decidiu conviver? E quais alternativas foram descartadas — modularizar o monolito, extrair só o gargalo, ou simplesmente **não fazer nada** (por que isso não serve)?

5. **Quem é afetado e quem revisa** — quem são os autores do doc, e quais times/áreas devem revisar (segurança, infraestrutura/plataforma, times que consomem as APIs do monolito)? Alguém fora do time depende de algo que vai mudar?

Duas coisas menores, se souber já responde junto: existe um **template de design doc** na wiki/drive de vocês que eu deva seguir? E onde salvo o arquivo — sugiro `docs/design/`, mas o repositório está vazio e não tenho precedente.

Com as respostas de 1 a 4 eu já consigo escrever um documento honesto (incluindo diagrama C4 da arquitetura-alvo e um diagrama de sequência de um fluxo crítico, se fizer sentido). Se algum ponto ainda estiver em aberto no time, me diz — vira uma seção de *Questões em aberto*, que é melhor do que texto inventado.
