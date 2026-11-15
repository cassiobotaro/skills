Não escrevi o ADR ainda, e não criei nenhum arquivo. Um ADR registra uma decisão que o time já tomou, com os motivos reais. Se vocês ainda não bateram o martelo entre Kafka e RabbitMQ, não há decisão para registrar. Qualquer texto que eu escrevesse agora teria que inventar o vencedor e as razões dele, e isso estraga o log: quem ler daqui a um ano vai confiar em um "porquê" que ninguém de fato discutiu.

Dois caminhos, conforme o momento de vocês:

1. **Ainda comparando as opções.** Isso é design doc, não ADR. Ele cobre requisitos (volume, ordenação, retenção/replay, latência, operação), as alternativas e os trade-offs de cada uma. Se a skill `design-doc` estiver instalada, posso conduzir isso com vocês. Quando a escolha for feita, ela vira um ADR curto.

2. **Já existe uma proposta concreta aguardando aprovação** (por exemplo, "queremos Kafka" e falta o aval de alguém). Aí posso escrever um ADR com status `Proposed`. Para isso preciso de respostas a estas perguntas:
   - Qual é a opção proposta e o que muda em relação ao que existe hoje? Por que agora?
   - Que alternativas foram consideradas além dela, e por que perderam?
   - Qual desvantagem o time aceita ao escolher essa opção?
   - Quem ainda precisa concordar?

Quando vocês decidirem, é só me dizer a escolha e os motivos. Aí o ADR sai como `Accepted`, no log do projeto.
