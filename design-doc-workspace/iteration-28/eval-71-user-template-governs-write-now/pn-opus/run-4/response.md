O documento está salvo em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`, com Estado "Rascunho".

**Formato:** mantive as seções do template, na ordem dele. Fiz duas escolhas sozinho:

- **Seção a mais:** incluí "Trade-offs e alternativas consideradas" entre Proposta e Riscos. O template não tem onde registrar o +5ms nem as alternativas que vocês descartaram (não fazer nada, deduplicar no consumidor, idempotência nativa do Kafka). Se o time de arquitetura não aceitar seção extra, dá para passar esse conteúdo para dentro de Proposta.
- **Número do documento:** usei DD-2026-001 porque não havia nenhum outro doc em `docs/design/` para seguir a numeração. Se já existe uma sequência em outro lugar, é só trocar.

**O que usei:** só o que você disse. Motivação com os 4% e as duas reclamações do financeiro, o fluxo com o Redis e as 24h, o custo de +5ms e a meta de menos de 0,1%.

**O que ficou para você:** você não deu riscos além da latência nem um plano de rollout. Essas seções têm só o que foi estabelecido e apontam para as perguntas abertas. Deixei 11 perguntas no final. As mais importantes:

- **Origem da chave idempotente:** quem gera a chave, e se ela se repete em todo reenvio. A proposta inteira depende disso.
- **Redis indisponível:** o serviço deixa o evento passar (aceitando duplicatas) ou bloqueia a ingestão?
- **Falha depois de gravar a chave:** se o serviço grava a chave no Redis e a publicação no Kafka falha, o reenvio seguinte seria descartado e o evento se perderia.
- **Janela de 24h:** de onde vem o valor, e se os reenvios que geram os 4% caem todos dentro dela.
- **Rollout e rollback.**
- **Revisores:** o campo está vazio. Sugeri o time dono do Redis e do Kafka e alguém do financeiro.

As outras cobrem o orçamento de latência, como os 4% foram medidos, o dimensionamento do Redis e a correção dos relatórios de faturamento já afetados.
