Li o template e você já me deu material para a **Motivação**, a **Proposta** e as **Métricas de sucesso**. Três seções obrigatórias do template ainda não têm conteúdo, e o time de arquitetura vai cobrar todas elas. Prefiro perguntar a inventar:

1. **Riscos.** O que vocês enxergam que pode dar errado com o serviço, e como pretendem mitigar cada risco? Os +5ms eu vou registrar como custo aceito, não como risco. Se o time ainda não discutiu riscos, me diga, e eu registro isso em Perguntas abertas.
2. **Plano de rollout.** Como o serviço vai entrar em produção? Quero saber as fases (por exemplo, shadow mode, percentual de tráfego, produtor por produtor), o critério para avançar de uma fase para a próxima e o critério de rollback. Se isso ainda não foi definido, também vai para Perguntas abertas.
3. **Perguntas abertas.** Tem algo que o time já sabe que ainda não sabe? Por exemplo, de onde vem a chave idempotente de cada evento, ou se a janela de 24h foi validada contra o intervalo real dos reenvios.

E três pontos menores:

4. **Métricas.** Além de duplicatas abaixo de 0,1%, vocês querem um teto de latência (p99?) ou outro número que defina sucesso? E como os 4% foram medidos? Eu gostaria de descrever a mesma medição como base da meta.
5. **"Não fazer nada".** Vocês consideraram corrigir os relatórios de faturamento depois, sem mexer no pipeline? Se sim, por que essa opção foi descartada? Pretendo criar uma seção **Alternativas consideradas** depois de Proposta, porque o template não tem lugar para as duas alternativas que vocês discutiram. As seis seções do template ficam intactas e na ordem original. Você aceita esse acréscimo?
6. **Cabeçalho.** Quem são os **Revisores**? E o ID: como não existe nenhum doc em `docs/design/` além do template, posso usar `DD-2026-001`?

Com essas respostas eu escrevo o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`.
