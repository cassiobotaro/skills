Documentei a decisão em `docs/adr/0001-rabbitmq-em-vez-de-kafka.md`. O repositório estava vazio, então criei a pasta `docs/adr/` e escolhi um formato simples de ADR. Não fiz commit.

O documento tem status "Aceita", datado de 2026-11-22, e as seções de contexto, decisão, justificativa e consequências. Os três motivos que você deu (experiência da equipe, menos de 100 msg/s e nenhuma retenção de eventos) aparecem na justificativa. A perda do replay está registrada como trade-off aceito. Deixei também escrito que qualquer necessidade futura de replay será uma nova decisão, com um novo ADR.

Acrescentei por conta própria uma consequência negativa que você não citou: se o volume crescer muito acima do previsto, pode ser preciso reavaliar. Se não quiser essa linha, é só removê-la.
