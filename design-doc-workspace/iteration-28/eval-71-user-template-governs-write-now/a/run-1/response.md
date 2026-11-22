Rafael, escrevi o doc em `docs/design/servico-de-deduplicacao-de-eventos.md`, seguindo o `TEMPLATE.md` na ordem original. Ele mantém o cabeçalho, Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas. O doc ainda tem lacunas, descritas abaixo.

**Desvio do template que você precisa aceitar:** o template não tem lugar para as alternativas que você descreveu, então criei a seção "Alternativas consideradas" logo depois da Proposta. Ela tem as duas alternativas descartadas, a escolhida, e "não fazer nada" ligado aos 4% de duplicatas. O trade-off dos +5ms ficou como subseção da Proposta. Se o time de arquitetura preferir outro lugar para esses dois, é só mover.

**O que ficou vazio, porque você não me deu a informação:**
- **Riscos:** só consta a latência de +5ms. Não inventei riscos nem mitigações.
- **Plano de rollout:** ficou como "ainda não definido".
- **Revisores:** campo em branco.
- **Número do documento:** ficou como `DD-2026-<seq>`, porque não há outros docs no diretório para continuar a sequência.

**Métricas de sucesso:** ficaram a meta de duplicatas abaixo de 0,1% (hoje 4%) e a latência próxima da estimada. A forma de medir e o prazo para atingir a meta ficaram como pergunta.

As 9 perguntas estão no fim do doc, agrupadas por seção do template. As mais importantes são:
- O que acontece se o Redis cair: a ingestão passa sem deduplicar ou fica bloqueada?
- Como tratar um reenvio que chega depois das 24h?
- O rollout é de uma vez ou em fases, e qual o critério de rollback?

Não coloquei diagrama, porque não sei quais tecnologias e protocolos entrariam nas caixas e nas setas. Se você me passar esses dados, eu incluo.

Também mantive a data de criação como 2026-11-22 e o estado como "Rascunho".
