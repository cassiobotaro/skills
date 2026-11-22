Ainda não criei o arquivo. O template tem duas seções que a conversa não preencheu, e o campo de ID também está em aberto. Seguir o template à risca significa não deixar buraco nem inventar conteúdo, então preciso das suas respostas antes de escrever.

**O que já tenho** (Motivação, Proposta, Métricas de sucesso e parte de Riscos):
- 4% de duplicatas no mês passado, vindas de reenvio em retry, inflando o faturamento. O financeiro reclamou duas vezes.
- Serviço entre o ingestor e o Kafka, com a chave idempotente no Redis por 24h, descartando repetidos.
- Alternativas descartadas: deduplicar no consumidor e usar a idempotência nativa do produtor Kafka.
- Trade-off aceito: mais um salto no caminho crítico, cerca de +5ms.
- Meta: duplicatas abaixo de 0,1%.

**O que preciso que você responda:**

1. **Plano de rollout:** como o serviço entra em produção? Por exemplo, em fases ou por produtor, e com qual critério para avançar de uma fase para a próxima. E qual é o critério e o caminho de rollback?
2. **Riscos:** além dos +5ms, o que pode dar errado e como vocês mitigam? Em especial, o que acontece com a ingestão se o Redis ficar indisponível ou perder dados: ela segue sem deduplicar (fail-open), ou para (fail-closed)? E o que o serviço faz com um duplicado que chega depois de 24h?
3. **Métricas de sucesso:** a meta de <0,1% fica como está. Como e onde vocês medem a taxa de duplicatas, e a partir de quando? Quer incluir um limite para a latência (os +5ms estimados) ou só a meta de duplicatas?
4. **Perguntas abertas:** há algo que vocês ainda não decidiram? Por exemplo, qual é a chave idempotente (campo do evento ou ID do produtor) e se o serviço escala de forma independente. Se não houver nada, registro que não há.
5. **Cabeçalho:** qual é o número de sequência do DD-2026-<seq>? Quem são os revisores? A pasta só tem o `TEMPLATE.md`, então não consigo deduzir a sequência. Se ainda não houver revisores definidos, deixo o campo vazio.

**Um ponto sobre o formato:** o template não tem seção para objetivos nem para alternativas consideradas, e você me deu as duas coisas. Para não perder esse conteúdo, minha proposta é manter a estrutura e a ordem do template e acrescentar uma seção "Alternativas consideradas" logo depois de "Proposta". A meta de <0,1% já vai em "Métricas de sucesso". Se o time de arquitetura não aceita seções extras, me avise e eu embuto as alternativas dentro de "Proposta".

Com essas respostas, escrevo o doc em `docs/design/`, com você (Rafael Nunes) como autor.
