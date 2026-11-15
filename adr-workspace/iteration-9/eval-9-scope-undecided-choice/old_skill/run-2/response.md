Ainda não escrevi o ADR. Um ADR registra uma decisão e as razões reais do time, e hoje não tenho nenhuma das duas coisas. Se eu escolhesse Kafka ou RabbitMQ por conta própria, teria que inventar o contexto e os trade-offs. Esse é justamente o tipo de justificativa que contamina um log de decisões.

Não há log de ADRs neste repositório. Quando a decisão estiver clara, eu crio `doc/adr/` com o ADR 0001 padrão ("Record architecture decisions"), e este ADR vira o 0002.

Preciso de algumas respostas:

1. **Qual é o contexto do barramento de eventos?** Quem produz e quem consome, qual o volume e a latência esperados, e se vocês precisam reler ou reprocessar eventos antigos (replay) ou só entregar mensagens.
2. **Quais restrições pesam na escolha?** Por exemplo, a experiência do time com cada ferramenta, o custo de operar a infraestrutura (própria ou gerenciada), requisitos de ordenação e de retenção, e o que já existe em produção hoje.
3. **Que alternativas vocês consideraram além dessas duas, e o que cada uma deixa de bom ou de ruim na avaliação do time?** (Isso inclui a opção de não adotar nada agora.)
4. **A decisão sai agora ou fica em aberto?**
   - Se ainda não está decidida, posso escrever o ADR com status `Proposed`. Ele registra o contexto, as opções e os trade-offs, e a seção Decision fica para quando o time fechar. Isso só funciona se o time me disser qual opção está propondo.
   - Se vocês já bateram o martelo, me diga qual foi a escolha e por quê, e eu escrevo como `Accepted`.

Com essas respostas eu escrevo o ADR em português, mantendo os títulos de seção e o status em inglês, que é o que o `adr-tools` espera.
