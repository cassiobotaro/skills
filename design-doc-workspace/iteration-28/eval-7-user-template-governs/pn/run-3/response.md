Ainda não criei o arquivo. O template exige Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas, e o que você me passou cobre só Motivação e Proposta, mais um pedaço de Riscos (os +5ms). Prefiro não inventar o resto, porque o time de arquitetura vai ler essas seções com atenção. Pode responder em tópicos curtos:

1. **Riscos.** Além dos +5ms no caminho crítico, o que acontece se o Redis cair ou ficar lento? O serviço deixa passar eventos sem deduplicar (*fail-open*) ou barra a ingestão (*fail-closed*)? Há outros riscos que vocês já levantaram, por exemplo descartar por engano um evento legítimo, ou a janela de 24h não cobrir um reenvio tardio?
2. **Plano de rollout.** Como isso entra em produção? Por exemplo, shadow mode, depois uma parte dos produtores, depois todos. Qual critério decide avançar de fase e qual decide o rollback?
3. **Métricas de sucesso.** Além de duplicatas abaixo de 0,1% (medido como os 4% do mês passado?) e +5ms, vocês querem acompanhar mais algo? Os +5ms são p50 ou p99? Em que prazo após o rollout vocês medem a meta?
4. **Perguntas abertas.** O que vocês ainda não sabem? Dois exemplos possíveis: quem gera a chave idempotente (os produtores já mandam uma?) e como o serviço dimensiona o Redis.
5. **Cabeçalho.** Quem são os revisores? A pasta só tem o template, então vou numerar como **DD-2026-001**, a menos que vocês usem outra numeração.

Com isso eu escrevo o doc em `docs/design/`. Vou seguir a ordem do template e registrar as duas alternativas descartadas dentro de Proposta. O template não tem seção própria para elas, e aviso quando eu fizer isso.
