O template exige seções que o seu relato ainda não cobre. A skill pede que eu pergunte antes de preencher, em vez de inventar conteúdo, então ainda não criei o arquivo.

**Lacunas do template:**

1. **Revisores:** quem revisa e de qual área? Imagino que entrem arquitetura, o time dono do Kafka/Redis e talvez o financeiro, mas os nomes precisam vir de você.
2. **Riscos:** o único custo que você citou foi o +5ms. Que outros riscos o time levantou, e qual a mitigação de cada um? Tem uma situação que o design abre e eu não consigo responder sozinho: se o Redis ficar indisponível, o serviço deixa passar os eventos (e as duplicatas voltam) ou bloqueia a ingestão? E um reenvio que chegue depois das 24h passa como evento novo. Isso já foi discutido?
3. **Plano de rollout:** como o serviço entra em produção? Por exemplo, primeiro só marcando duplicatas sem descartar, depois por produtor ou por percentual de tráfego. Qual critério libera cada fase e como se faz o rollback (desviar o ingestor direto pro Kafka de novo?)?
4. **Métricas de sucesso:** a meta de menos de 0,1% eu já tenho. Como vocês mediram os 4%, e a mesma medição vale para o 0,1%? Existe um teto de latência acima do qual o rollout para, ou os +5ms são só uma estimativa?

**Detalhe da proposta:**

5. **Chave idempotente:** de onde ela vem? O produtor já manda um ID no evento ou o serviço calcula a chave a partir do conteúdo?

**Estrutura:** o template não tem lugar para as alternativas descartadas (dedup no consumidor e idempotência nativa do produtor Kafka), nem para o "não fazer nada", nem para o trade-off aceito. Minha proposta é acrescentar duas seções, **Alternativas consideradas** e **Trade-offs**, entre Proposta e Riscos. As seis seções do template continuam na ordem original. Se o time de arquitetura não aceitar seções a mais, eu coloco esse conteúdo dentro de Proposta. Qual das duas opções você prefere?

O arquivo vai se chamar `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. É o primeiro doc da pasta, por isso a sequência começa em 001. Pode ser assim, ou vocês já têm uma numeração em outro lugar?

O que você não souber responder agora vai para Perguntas abertas, em vez de virar texto inventado.
