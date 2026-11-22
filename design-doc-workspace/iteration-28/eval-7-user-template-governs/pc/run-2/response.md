Ainda não criei o arquivo. Você deu a motivação, a proposta, as alternativas, o trade-off de latência e a meta. Faltam o conteúdo de duas seções do template (Riscos e Plano de rollout) e alguns detalhes da Proposta. Se eu preenchesse isso por conta própria, o time de arquitetura leria como avaliação de vocês.

**Riscos.** Você citou só o +5ms de latência. Quais outros riscos o time enxerga e como pretendem mitigar cada um? Dois exemplos do que eu perguntaria:
- O que acontece com a ingestão se o Redis ficar indisponível? O serviço deixa passar (fail-open, aceita duplicatas) ou bloqueia (fail-closed)?
- O serviço novo está no caminho crítico. O que vocês decidiram sobre a disponibilidade dele?

**Plano de rollout.**
- Como entra em produção? Tem fases, por exemplo shadow mode só medindo duplicatas ou um percentual de produtores?
- Qual o critério para avançar de uma fase para a próxima?
- Qual o critério e o mecanismo de rollback?

**Proposta.** Para o texto e os diagramas eu preciso de:
- Qual é a chave idempotente? Vem do produtor (um header ou um campo do evento) ou o serviço a calcula?
- O serviço é síncrono, com o ingestor chamando e esperando a resposta? Que tecnologia e protocolo vocês usam entre os componentes? Não quero chutar o que vai na caixa e na seta do diagrama.
- A checagem e o registro da chave são atômicos, por exemplo um `SET NX` com TTL de 24h? Ou isso ainda não foi decidido?

**Métricas de sucesso.** Além de duplicatas abaixo de 0,1% (hoje 4%), vocês querem um limite para a latência adicionada, ou o +5ms é só estimativa? Querem acompanhar mais algum número, como uma queda nas reclamações do financeiro?

**Outros dados.**
- Quem são os revisores do cabeçalho?
- Posso usar `DD-2026-001` como número? A pasta só tem o template, então não há sequência anterior.
- O que ainda está em aberto para a seção de Perguntas abertas?

Se preferir o documento já, com o que está definido, me avise. Nesse caso eu escrevo, deixo cada seção sem resposta marcada como pendente e registro as perguntas acima em Perguntas abertas.

Os pontos que você já deu (4% de duplicatas, as alternativas descartadas, o +5ms, a meta de 0,1%) entram no documento como estão. O template não tem seção de alternativas. Quando eu escrever, vou criar uma seção "Alternativas consideradas" para elas, mantendo as demais seções na ordem do template, e aviso você disso.
