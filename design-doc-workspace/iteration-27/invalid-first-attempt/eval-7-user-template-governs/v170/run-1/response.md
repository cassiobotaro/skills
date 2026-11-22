Salvei o doc em `docs/design/DD-2026-001-servico-de-deduplicacao-de-eventos.md`. Não rodei commit.

**Template.** Usei as seis seções do TEMPLATE.md, na mesma ordem, com o mesmo cabeçalho e a tabela de metadados. Como o template não tem seção de alternativas, as duas que vocês descartaram ficam em "Alternativas consideradas", dentro de **Proposta**. O trade-off dos +5 ms fica na mesma seção, logo depois. O número é DD-2026-001 porque `docs/design/` só tinha o template. Confira se a numeração está certa.

**Conteúdo.** Os números (4% de duplicatas, TTL de 24h, +5 ms, meta abaixo de 0,1%) são só os que você deu.

**Itens que escrevi sem você ter dito.**
- O plano de rollout é uma proposta minha: modo sombra, depois descarte em parte do tráfego, depois descarte em todo o tráfego. O texto avisa que precisa de revisão.
- A tabela de riscos traz alguns que você não citou: Redis fora do ar, falha na publicação no Kafka depois de a chave ser gravada (o retry seria descartado e o evento se perderia) e reenvio depois de 24h.
- Na métrica das reclamações do financeiro, a meta de 0 é minha. Você só informou o número atual (2).

**Pendências para você.**
- O campo **Revisores** está vazio. Preencha antes de mandar para a arquitetura.
- A seção de perguntas abertas lista o que falta decidir. As mais importantes são qual campo é a chave idempotente, se o serviço deixa o evento passar ou o rejeita quando o Redis cai, e a topologia do Redis.
