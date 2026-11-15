Ainda não vou criar o ADR. Um ADR registra uma decisão que o time já tomou, com as razões reais dela. Se eu escrevesse agora "Kafka ou RabbitMQ", teria que inventar a decisão e os motivos, e isso estragaria o log. Por isso não abri o log nem criei nenhum arquivo.

Como a escolha ainda está aberta, vejo dois caminhos:

1. **Esperar o martelo.** Quando vocês decidirem, me diga qual escolheram e por quê. Preciso de três coisas: o que vocês vão fazer, as forças em jogo (volume e padrão de eventos, requisitos de ordenação e retenção, experiência do time, custo operacional) e o que o time aceitou perder com a escolha. Aí eu escrevo o ADR como `Accepted`.
2. **ADR `Proposed`.** Se já existe uma proposta concreta, por exemplo "propomos Kafka" ou "propomos RabbitMQ", e ela está só esperando aprovação, eu registro como `Proposed` com as razões que vocês me passarem. Depois o status vira `Accepted` ou o ADR é substituído.

Se o que vocês precisam agora é comparar as duas opções e levantar as perguntas em aberto, isso é um design doc (a skill `design-doc`), não um ADR. Cada decisão que sair dele pode virar um ADR depois.

Qual dos dois caminhos faz mais sentido? Se for o segundo, me diga qual é a proposta e os motivos dela.
