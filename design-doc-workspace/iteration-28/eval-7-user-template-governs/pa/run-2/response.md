Li o template e ainda não criei o arquivo. Faltam informações que o template exige e que você não passou. Prefiro perguntar a inventar conteúdo, porque o time de arquitetura vai ler cada seção.

**Plano de rollout** (seção obrigatória, sem nenhuma informação sua até agora)
1. Como o serviço entra em produção? Por exemplo: modo sombra (só marca duplicatas, sem descartar), depois uma fração dos produtores, depois todos. Ou outro caminho?
2. Qual é o critério para avançar de uma fase para a próxima, e qual é o gatilho de rollback?

**Riscos** (você deu só o +5ms de latência)
3. O que acontece se o Redis cair ou ficar lento? O serviço deixa passar eventos (*fail-open*, volta a ter duplicatas) ou bloqueia a ingestão (*fail-closed*)? Qual foi a decisão do time?
4. Há outros riscos que vocês já discutiram? Dois exemplos: a janela de 24h não cobrir reenvios mais tardios, e perda de chaves no Redis (failover, eviction).

**Métricas de sucesso**
5. Além de duplicatas abaixo de 0,1%, existe um teto de latência (o +5ms é um limite ou só uma estimativa) ou de disponibilidade para o serviço?

**Cabeçalho**
6. Quem são os revisores? E qual é o número do doc? A pasta só tem o template, então não consigo continuar uma sequência. Posso usar `DD-2026-001` se você não tiver outro.

**Um ponto sobre o formato**
As alternativas descartadas (deduplicação no consumidor e idempotência nativa do produtor Kafka) não têm seção no template. Para não perder esse conteúdo, quero incluir uma seção extra, "Alternativas consideradas", entre Proposta e Riscos. O resto do template fica intacto, na mesma ordem. Se o time de arquitetura não aceita seções extras, posso colocar as alternativas dentro de Proposta. Qual você prefere?

Com essas respostas eu escrevo o doc em `docs/design/`. Se algum item ainda estiver em aberto, ele vai para "Perguntas abertas".
