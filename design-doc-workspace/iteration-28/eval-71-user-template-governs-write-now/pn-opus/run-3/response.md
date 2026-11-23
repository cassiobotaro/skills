Salvei o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Ele tem as seis seções do `TEMPLATE.md`, na mesma ordem. Como a pasta não tinha nenhum doc antes, comecei a numeração em DD-2026-001.

**Onde fugi do template:** ele não tem lugar para o trade-off aceito nem para as alternativas que vocês discutiram. Para não mudar as seções principais, que é o formato que a arquitetura cobra, coloquei os dois como subseções dentro de **Proposta**. Nas alternativas incluí "não fazer nada", com a dor que você descreveu (4% de duplicatas e duas reclamações do financeiro). Se preferir tirar essas subseções ou mudar de lugar, me avisa.

**O que ficou incompleto porque depende de você:**
- **Riscos:** só registrei o risco que você deu, os +5 ms no caminho crítico. Não inventei outros riscos nem mitigações. A seção remete para as perguntas abertas.
- **Plano de rollout:** está como "ainda não definido".
- **Revisores:** está "a definir".

**Perguntas abertas no fim do doc:**
1. De onde vem a chave idempotente? Todos os produtores já mandam uma? O que o serviço faz com evento sem chave?
2. Que dado justifica a janela de 24h? Quantos reenvios chegam depois disso?
3. Se o Redis cair, o serviço deixa os eventos passarem ou trava a ingestão?
4. Em que ordem o serviço registra a chave e publica no Kafka? Se ele registrar antes e a publicação falhar, o reenvio seria descartado e o evento se perderia.
5. Qual é o volume de eventos e quanta memória o Redis precisa? Esse Redis é novo ou compartilhado com outro time?
6. Como fica o rollout: fases, critério para avançar e rollback?
7. Como vamos medir a taxa de duplicatas depois do serviço? É a mesma medição que deu os 4%? E como confirmamos os +5 ms?
8. Quem revisa? Sugeri o time dono do Kafka e do Redis, os times produtores e o financeiro.
9. Os relatórios de faturamento que já saíram com duplicatas precisam ser corrigidos?

Quando você responder, eu passo as respostas para as seções certas (principalmente Riscos e Rollout) e tiro essas perguntas da lista.
