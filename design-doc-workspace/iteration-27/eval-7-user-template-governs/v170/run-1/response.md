Ainda não criei o arquivo. O template tem seções que a conversa não preencheu, e prefiro não inventar conteúdo nelas. O `docs/design/` só tem o `TEMPLATE.md`, então também não consigo deduzir a numeração.

Já tenho material para Motivação (4% de duplicatas, faturamento inflado, financeiro reclamou duas vezes), Proposta (serviço entre o ingestor e o Kafka, chave idempotente no Redis por 24h, descarta repetidos), Métricas (duplicatas abaixo de 0,1%) e as alternativas descartadas. O template não tem seção para as alternativas, então vou acrescentar uma seção "Alternativas consideradas" depois de Proposta, com o resto do esqueleto na ordem original. Aviso aqui para você aceitar ou vetar.

Faltam estas respostas:

1. **Número do doc:** qual é o `DD-<ano>-<seq>`? Pelo ano seria DD-2026-NNN, mas não sei qual é o próximo número.
2. **Revisores:** quem entra no cabeçalho (arquitetura, financeiro, outros)?
3. **Riscos:** além dos +5ms no caminho crítico, que riscos vocês já discutiram? Em especial:
   - O que acontece se o Redis cair ou ficar lento: o serviço deixa passar duplicatas (fail-open) ou bloqueia a ingestão (fail-closed)?
   - Como o serviço trata a janela entre gravar a chave e publicar no Kafka? Se o serviço falhar no meio, o evento pode se perder ou duplicar.
   - Eventos repetidos depois de mais de 24h passam. Isso é aceitável?
   - Qual é o plano para o serviço novo ser um ponto único de falha?
4. **Plano de rollout:** como vocês pretendem entrar em produção (modo sombra que só mede duplicatas, percentual de tráfego, por produtor)? Qual é o critério para avançar de fase e qual dispara o rollback?
5. **Detalhes da proposta que o doc precisa:**
   - Como a chave idempotente é formada: o produtor já manda um ID ou o serviço calcula um hash?
   - Qual é a tecnologia ou protocolo entre ingestor e serviço?
   - Existe meta de latência (p99) além dos +5ms estimados?

Se alguma resposta ainda for desconhecida, diga isso e eu registro em **Perguntas abertas**. Não vou preencher a seção com suposição.
