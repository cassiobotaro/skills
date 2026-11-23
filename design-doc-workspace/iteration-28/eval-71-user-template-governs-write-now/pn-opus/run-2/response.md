Rafael, o doc está pronto em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`, com estado Rascunho. Ele segue as seções do `TEMPLATE.md` na ordem original. Usei só o que você me passou, e o que faltava virou pergunta no final.

**Duas seções a mais que o template não tem.** O template não tem onde registrar trade-offs nem alternativas, e você me passou os dois. Então coloquei uma subseção **Trade-offs** dentro de *Proposta* e uma seção **Alternativas consideradas** entre *Proposta* e *Riscos*. As alternativas são três: não fazer nada, deduplicar no consumidor e usar a idempotência nativa do produtor Kafka. Se a arquitetura exigir só as seções do template, dá para passar os trade-offs para *Riscos* e as alternativas para dentro de *Proposta*, mas o porquê da decisão fica menos visível.

**Seções com pouco conteúdo:**
- **Riscos:** tem só a latência de +5ms e o limite da janela de 24h. Nenhum dos dois tem mitigação ainda.
- **Plano de rollout:** você não me passou nada, então a seção só remete às perguntas abertas.
- **Revisores:** o campo ficou vazio.

Na *Proposta* incluí um diagrama de sequência em Mermaid. Ele não indica protocolo nem tecnologia, porque você não definiu esses pontos.

**As 9 perguntas abertas, em resumo:**
1. Todos os produtores já mandam a chave idempotente, e como ela é formada?
2. Por que 24h, e existem reenvios depois desse prazo?
3. Se o serviço ou o Redis cair, a ingestão para ou os eventos passam sem deduplicação?
4. Que outros riscos existem, e como cada um será mitigado?
5. De onde vem a estimativa de 5ms, e existe um teto de latência?
6. Como vai ser o rollout: fases, critério para avançar e rollback?
7. Como os 4% foram medidos, e a meta de 0,1% vai usar o mesmo método?
8. Quem revisa? Sugeri a arquitetura, o time do Kafka e do Redis, e alguém do financeiro.
9. Usei o número DD-2026-001 porque é o primeiro doc da pasta. Existe uma sequência em outro lugar que ele deveria seguir?

Não fiz commit.
