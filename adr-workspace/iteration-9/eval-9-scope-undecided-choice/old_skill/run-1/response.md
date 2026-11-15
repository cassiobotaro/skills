Ainda não escrevi o ADR. Um ADR registra uma decisão e as razões reais do time, e hoje eu não tenho nenhuma das duas coisas. Não existe escolha entre Kafka e RabbitMQ, e eu não conheço as forças do seu contexto. Se eu escrevesse agora, teria que inventar o motivo, o volume e as consequências, e isso estragaria o registro.

Também não encontrei nenhum log de decisões no repositório. Quando o ADR for escrito, vou criar `doc/adr/` com o ADR 0001 ("Registrar as decisões de arquitetura") e a sua decisão entra como 0002.

Para eu escrever, preciso de respostas para estas perguntas:

1. **Em que ponto está a decisão?** Vocês já têm uma inclinação, mesmo que ninguém tenha fechado? Ou querem registrar a discussão em aberto, com o ADR em status `Proposed`, para o time fechar depois? Se for isso, eu documento as opções e o que está em jogo, sem declarar um vencedor.
2. **Por que decidir agora?** O que há de errado ou faltando hoje no barramento de eventos (ou na falta dele)? Quais são os requisitos que pesam: volume de mensagens, necessidade de replay ou retenção de eventos, garantias de ordenação, número de consumidores, latência?
3. **Quais alternativas estão na mesa?** Além de Kafka e RabbitMQ, existe mais alguma opção (SQS, NATS, Pub/Sub etc.)? A experiência operacional do time com cada uma conta como fator?
4. **Qual custo o time aceita pagar em cada caminho?** Por exemplo, a complexidade operacional do Kafka ou abrir mão do replay no RabbitMQ. E quem ainda não concordou?

Com essas respostas eu escrevo o ADR em português, com o status `Proposed` ou `Accepted` conforme o caso.
