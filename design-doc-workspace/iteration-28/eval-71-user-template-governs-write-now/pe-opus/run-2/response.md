O doc está salvo em `docs/design/DD-2026-001-servico-deduplicacao-eventos.md`. Ele segue o `TEMPLATE.md`, com as seções na mesma ordem e no estado Rascunho. Usei a numeração DD-2026-001 porque é o primeiro doc da pasta.

Só escrevi o que você me passou: o problema, os 4% de duplicatas, as duas reclamações do financeiro, o desenho com Redis e janela de 24h, o custo de +5ms e a meta de 0,1%. Coloquei também um diagrama de sequência do fluxo seguido do texto que o explica, como o template pede. Tirei do texto as frases que eu tinha deduzido sem você ter dito, por exemplo que o ingestor publica direto no Kafka hoje ou que os consumidores não mudam.

**Um desvio do template, para você aprovar:** ele não tem seção para alternativas nem para trade-off. Para não perder o que vocês discutiram:
- O trade-off aceito virou uma subseção dentro de **Proposta**.
- Criei a seção **Alternativas consideradas** entre Proposta e Riscos, com "não fazer nada", deduplicar no consumidor e idempotência nativa do produtor.

Se o time de arquitetura não aceitar seção extra, dá para mover as alternativas para dentro de Proposta.

**Seções que ficaram sem conteúdo:**
- **Riscos:** você só citou o salto extra na latência, que é um custo aceito e não um risco com mitigação. Não inventei riscos; a seção aponta para as perguntas abertas.
- **Plano de rollout:** você não falou nada sobre fases, critério de avanço ou rollback, então a seção também aponta para as perguntas.
- **Revisores:** está vazio no cabeçalho.

As 9 perguntas abertas no final, para quando você tiver tempo:
1. Quem revisa o doc, e se o financeiro entra.
2. De onde vem a chave idempotente de cada evento.
3. Por que a janela é de 24h, e o que acontece com um reenvio que chega depois dela.
4. Se a chave é gravada no Redis antes ou depois de publicar no Kafka, e se a consulta e a gravação precisam ser atômicas. Deixei uma nota no diagrama marcando isso como em aberto.
5. Quais riscos e mitigações vocês já identificaram, e se o serviço deixa passar ou bloqueia o evento quando falha.
6. Como vai ser o rollout em fases e o rollback.
7. Como os 4% foram medidos, e se o mesmo método vai checar a meta de 0,1%.
8. A que percentil se referem os +5ms, e se existe um teto de latência.
9. Que outros times são afetados: quem opera o Redis, o Kafka e o ingestor.

Não fiz commit.
