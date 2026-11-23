Li o template e o contexto que você passou. Ainda não criei o arquivo, porque três seções do template ficaram sem conteúdo e prefiro não inventar nada no lugar. Pelo que você já disse, consigo escrever Motivação, Proposta e o trade-off dos +5ms. Preciso destas respostas:

**Riscos** (você só citou a latência de +5ms)
1. O que acontece com a ingestão se o Redis ou o serviço de deduplicação cair? O serviço deve falhar aberto (deixa passar duplicatas) ou fechado (bloqueia a ingestão)?
2. Que outros riscos o time já levantou, por exemplo perda dos dados do Redis ou duplicata que escapa depois das 24h? Se não discutiram, registro como pergunta aberta.

**Plano de rollout**
3. Como isso entra em produção? Por exemplo: modo sombra só contando duplicatas, depois uma parcela do tráfego, depois 100%. Qual é o critério para avançar de fase e qual é o gatilho de rollback?

**Métricas de sucesso**
4. A meta de duplicatas abaixo de 0,1% (contra os 4% medidos) está registrada. Há um teto de latência além dos +5ms estimados? E como vocês vão medir a taxa de duplicatas, com a mesma consulta do mês passado?

**Cabeçalho**
5. Quem são os revisores? Posso deixar o campo vazio.
6. A numeração é DD-2026-001? `docs/design/` só tem o TEMPLATE.md, então não há sequência anterior para eu continuar.

**Proposta**
7. Qual é a chave idempotente? Vem do produtor (um `event_id`) ou o serviço a calcula? Se o Redis confirma que a chave é nova mas o envio ao Kafka falha, o serviço remove a chave ou o retry é descartado? Se ainda não decidiram, vira pergunta aberta.

Também preciso de uma decisão sobre a estrutura. O template não tem lugar para as alternativas que vocês descartaram (deduplicar no consumidor e usar a idempotência nativa do produtor Kafka) nem para a meta. Minha sugestão é manter as seções do template na ordem e acrescentar duas: **Alternativas consideradas**, depois de Proposta, e **Objetivos**, antes dela. Se o time de arquitetura não aceitar seções extras, coloco as alternativas dentro de Proposta e a meta em Métricas. Qual você prefere?
