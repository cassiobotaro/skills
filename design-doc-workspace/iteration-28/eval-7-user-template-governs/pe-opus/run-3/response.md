Li o template em `docs/design/TEMPLATE.md`. A motivação, a proposta, as alternativas, o trade-off e a meta você já me deu. Faltam algumas seções obrigatórias do template, e eu não vou inventar nada para preenchê-las. Preciso de cinco respostas antes de escrever:

1. **Riscos.** O template pede cada risco com sua mitigação, e até agora nenhum foi citado. Quais riscos o time levantou? Uma pergunta específica: se o Redis ficar indisponível, o serviço deixa os eventos passarem (aceitando duplicatas) ou para a ingestão?

2. **Plano de rollout.** Como o serviço entra em produção? Quero saber as fases (shadow mode, percentual de tráfego, produtor por produtor…), o que permite avançar de uma fase para a próxima e como funciona o rollback.

3. **Chave idempotente.** Quem gera a chave, o produtor ou o ingestor, e em qual campo do evento ela vem? E de onde saiu a janela de 24h: ela cobre o maior intervalo de reenvio que vocês já observaram?

4. **Métricas de sucesso.** Como vocês mediram os 4% do mês passado? A mesma medição vai servir para verificar a meta de 0,1%? Os +5ms de latência também entram como métrica, com algum teto que dispare rollback?

5. **Cabeçalho.** Quem são os revisores, e de qual área cada um? O documento pode ser o `DD-2026-001`, já que é o primeiro da pasta?

Para registrar: o template não tem seção de alternativas. Para não perder o que vocês discutiram (deduplicar no consumidor, idempotência nativa do produtor Kafka, e também "não fazer nada"), minha proposta é acrescentar uma seção **Alternativas consideradas** logo depois de **Proposta**. O resto do template fica intacto. Se o time de arquitetura não aceitar seção extra, eu coloco as alternativas dentro de Proposta. Qual opção você prefere?

Se ainda não houver resposta para algum ponto, me diga e eu registro ele em **Perguntas abertas** em vez de deixar a seção vazia.
