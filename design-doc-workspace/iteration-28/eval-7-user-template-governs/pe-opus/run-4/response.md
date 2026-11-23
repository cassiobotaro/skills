Li o `TEMPLATE.md`. A pasta ainda não tem nenhum doc, então este seria o primeiro da sequência: proponho `DD-2026-001`, salvo em `docs/design/DD-2026-001-servico-deduplicacao-eventos.md`.

Você já me deu o que preciso para Motivação e Proposta, e também para as alternativas e o custo aceito. Duas seções que o template exige ainda não têm conteúdo: Riscos e Plano de rollout. Prefiro perguntar a preencher essas seções com coisas que eu inventaria:

1. **Riscos:** que riscos o time levantou, e qual a mitigação de cada um? Pergunto em especial por dois casos que não foram discutidos:
   - Se o Redis ficar indisponível, o serviço deixa o evento passar sem deduplicar (*fail open*) ou bloqueia a ingestão (*fail closed*)?
   - Existe reenvio que chegue depois da janela de 24h?
2. **Plano de rollout:** como o serviço entra em produção? Por exemplo, primeiro em modo sombra (só marca as duplicatas, sem descartar), depois produtor por produtor. Qual o critério para avançar de fase, e qual o caminho de rollback?
3. **Chave idempotente:** de onde ela vem? Os produtores já mandam um ID por evento, ou o serviço calcula a chave a partir do conteúdo? A Proposta depende dessa resposta.
4. **Métricas de sucesso:** como vocês mediram os 4%, e é assim que vão acompanhar a meta de 0,1%? Há prazo para atingir a meta, ou um limite de latência acima do qual o rollout para? Os +5ms são estimativa.
5. **Revisores e perguntas abertas:** quem revisa, e de qual área (Infra/SRE por causa do Redis, o time do Kafka, o financeiro)? E tem algo que vocês ainda não sabem e que deveria entrar em Perguntas abertas?

O template não tem lugar para as alternativas descartadas nem para o trade-off. Minha proposta é adicionar uma seção "Alternativas consideradas e trade-offs" logo depois de Proposta, mantendo todas as seções originais na mesma ordem. Esse é o único desvio do formato. Você acha que o time de arquitetura aceita? Se não aceitar, coloco esse conteúdo dentro de Proposta.

Se alguma pergunta ainda não tiver resposta, ela vai para Perguntas abertas.
