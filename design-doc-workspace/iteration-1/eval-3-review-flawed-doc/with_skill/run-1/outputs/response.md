Revisei o `docs/design/fanout-de-notificacoes.md`. O desenho técnico em si está coerente, mas o documento ainda não cumpre o principal papel de um design doc: registrar os **trade-offs** e o **porquê** da escolha. Apliquei direto tudo o que dá para melhorar sem inventar fatos seus, e deixei marcado no próprio doc (como "Nota do revisor") os pontos que dependem de você.

## O que já apliquei

- **Glossário** logo após o cabeçalho — SLA, CDC, DLQ, TPS, fanout, exchange e provider apareciam sem definição. Como o público provável inclui outros times, isso evita travar o leitor.
- **Separei "Visão geral" de "Contexto".** A visão geral estava num parágrafo só, misturando o propósito do doc com detalhes de implementação (exchange, DLQ, TPS, CDC). Agora a visão geral é curta e sem detalhes, e o contexto explica o modelo atual e *por que* ele trava (canais em série, um provider lento atrasa todos).
- **Texto explicativo após o diagrama** — antes o fluxograma vinha sem nenhuma prosa. Agora há um parágrafo descrevendo dispatcher, exchange, filas, workers e DLQ, e qual é o ganho central (desacoplar os canais).
- **Corrigi o diagrama:** o canal in-app não tinha DLQ, embora o texto diga "DLQ por canal". Completei com a `DLQ in-app` para o diagrama ficar consistente com a intenção descrita.
- **Reescrevi os objetivos** para nomearem o mecanismo (paralelizar canais, escalar workers por canal). Continuam sem número — marquei isso, ver perguntas abaixo.
- **Troquei o "Fora de escopo"**, que só negava os objetivos ("não deve ser lento", "não deve perder notificações") e não excluía nada de real. Coloquei exclusões concretas (não mexer na lógica de payload/provider; não incluir novos canais) — **confirme se estão certas.**
- **Plano:** mantive os 4 passos, adicionei criar as DLQs e sugeri manter o cron como fallback durante a migração do e-mail. Marquei a ausência de rollback.
- **Cabeçalho:** atualizei "Última atualização" para hoje (2026-06-07) e adicionei a linha de Revisores (a definir). Observação: o estado está "Em revisão" desde fevereiro — vale promover para o estado real quando fechar a revisão.

## O que preciso de você (não dá pra preencher sem inventar)

1. **Trade-offs da solução — o mais importante.** Hoje a solução aparece só como "mais escalável, robusta e fácil de manter", o que é um discurso de venda. O que piorou em troca? Por exemplo: passa a depender de um broker (RabbitMQ/SQS/Kafka?), some a ordem de entrega, ganha complexidade operacional (monitorar filas e DLQs), entrega passa a ser assíncrona. Qual custo o time aceitou conscientemente?

2. **Alternativas consideradas, incluindo "não fazer nada".** O que mais foi avaliado antes de escolher fanout com filas? (ex.: paralelizar dentro do próprio cron com pool de threads, aumentar a frequência do cron, outro modelo de mensageria.) E por que continuar como está hoje não é aceitável — qual é o custo concreto da lentidão atual?

3. **Números nos objetivos.** "Melhorar a performance" e "garantir o SLA" não são verificáveis. Qual é o SLA de entrega (ex.: 95% em até X minutos)? Qual a vazão atual e a meta (ex.: de N para M envios/min)? Sem isso não dá pra saber se o projeto deu certo.

4. **Broker e infraestrutura.** Qual broker será usado? Já existe na empresa ou é infra nova? Isso impacta o time de Infra/Plataforma — eles deveriam ser revisores (deixei a sugestão no cabeçalho).

5. **TPS por provider.** Você cita controle de TPS, mas não os limites. Quais são os TPS de cada provider (push, e-mail, in-app)? Isso dita quantos workers cada fila comporta.

6. **Rollback e critério de avanço entre etapas do plano.** Se a migração do e-mail der errado, como volta atrás? Qual sinal indica que uma etapa está saudável o suficiente para avançar?

7. **Como verificar em produção.** Quais métricas e alertas vão provar que está funcionando (profundidade das filas, taxa de DLQ, latência fim-a-fim)? Vale uma seção curta de observabilidade ligada ao SLA.

Me responde os pontos que conseguir e eu incorporo no documento — em especial 1, 2 e 3, que são o que dá valor de longo prazo ao doc.
