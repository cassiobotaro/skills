Li o template e não há outros docs em `docs/design/`, então este seria o primeiro (DD-2026-001). O template exige seções que a sua descrição ainda não cobre, e eu não quero inventar esse conteúdo nem deixar as seções com texto genérico. Antes de escrever, preciso de algumas respostas:

1. **Riscos**: além da latência de +5ms, o que pode dar errado, e como vocês mitigariam? Pense em Redis indisponível (o serviço deixa passar duplicatas ou bloqueia a ingestão?), perda de chaves no Redis, evento legítimo descartado por colisão de chave e o serviço virar ponto único de falha.
2. **Plano de rollout**: como entra em produção? Por exemplo, modo sombra (só mede, sem descartar), depois uma parcela dos produtores, depois todos. Qual é o critério para avançar de fase e qual é o gatilho de rollback?
3. **Métricas de sucesso**: a meta de duplicatas abaixo de 0,1% eu já tenho. Quero saber se há metas além dela, como um teto de latência (os +5ms são estimativa ou limite?) e disponibilidade. Também preciso saber onde e como as duplicatas são medidas hoje, para o doc dizer como a meta será verificada.
4. **Chave idempotente**: quem a gera, o produtor ou o ingestor? Isso afeta a proposta e o risco de colisão.
5. **Perguntas abertas**: o que ainda está em aberto? Por exemplo, dimensionamento do Redis, o que acontece com reenvios depois das 24h, ou a janela de 24h ser suficiente.
6. **Cabeçalho**: quem são os revisores? Posso numerar como DD-2026-001 e datar de hoje (2026-11-23), com estado "Rascunho"?

Se não souber alguma resposta, diga "em aberto". Nesse caso eu registro o item em **Perguntas abertas** e não invento uma resposta.

O template não tem lugar para as alternativas descartadas (dedup no consumidor e idempotência nativa do produtor Kafka). Pretendo manter a ordem e as seções do template e dobrar as alternativas dentro de **Proposta**, numa subseção "Alternativas consideradas". Assim não crio uma seção nova fora do formato da arquitetura. Se preferir outro encaixe, me avise.
