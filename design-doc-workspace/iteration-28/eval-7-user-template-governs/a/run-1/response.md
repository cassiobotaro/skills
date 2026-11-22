Rafael, ainda não salvei o doc. O template exige seções que a sua descrição não cobre, e eu não quero inventar o conteúdo delas nem deixá-las vazias. Já tenho o suficiente para a Motivação, a Proposta, as Métricas de sucesso (duplicatas abaixo de 0,1%) e o trade-off dos +5ms. Preciso de respostas para estas perguntas:

1. **Riscos:** o que pode dar errado com o serviço e como vocês mitigam cada risco? Hoje só tenho o +5ms de latência. Faltam, por exemplo:
   - o que acontece se o Redis cair ou ficar lento: o serviço deixa o evento passar (fail-open, com duplicatas) ou bloqueia a ingestão (fail-closed)?
   - o que acontece se o próprio serviço cair, já que ele entra no caminho crítico?
   - e o que acontece com um reenvio que chega depois das 24h?
2. **Plano de rollout:** como o serviço entra em produção? Preciso das fases (shadow mode, canário, por produtor etc.), do critério para avançar de uma fase para a outra e do critério e procedimento de rollback.
3. **Métricas de sucesso:** a meta é duplicatas abaixo de 0,1%, contra os 4% medidos. Como e onde isso vai ser medido, e em que prazo após o rollout? Existe também um limite aceitável de latência além dos +5ms estimados?
4. **Proposta:** quem gera a chave idempotente, o produtor ou o ingestor? Qual é o comportamento do serviço ao ver um repetido (descarta em silêncio, registra, devolve ack ao produtor)? Se quiser um diagrama de componentes, me diga as tecnologias e os protocolos de cada ligação. Não vou chutar esses detalhes.
5. **Cabeçalho:** quem são os revisores? Qual é o número do DD (`DD-<ano>-<seq>`)? Só existe o TEMPLATE.md em `docs/design/`, então não tenho a sequência.
6. **Perguntas abertas:** há algo que vocês ainda não decidiram e que deva entrar aqui?

**Uma divergência para você aprovar.** O template não tem lugar para as **Alternativas consideradas** (deduplicar no consumidor e usar a idempotência nativa do produtor Kafka, com os motivos do descarte) nem para as **Metas e fora de escopo**. Eu manteria a ordem e o esqueleto do template e adicionaria a seção de Alternativas entre a Proposta e os Riscos. Se o time de arquitetura não aceitar seções extras, me diga e eu incorporo as alternativas dentro da Proposta.

Com as respostas, escrevo o doc em português em `docs/design/`, com o estado em Rascunho e o Rafael Nunes como autor.
