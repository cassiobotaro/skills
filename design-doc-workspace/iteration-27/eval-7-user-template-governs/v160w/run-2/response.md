Salvei o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Não rodei o `unslop` nele.

O doc usa as seis seções do template, na ordem original. Como o time de arquitetura só aceita esse formato, não criei nenhuma seção de topo nova. As alternativas descartadas e o trade-off dos +5 ms entraram como subseções dentro de **Proposta**. A meta de menos de 0,1% de duplicatas entrou em **Métricas de sucesso**, com a linha de base de 4%.

- **Título e ID:** `docs/design/` só tinha o template, então usei `DD-2026-001`. Se o time numera de outra forma, ajuste o ID.
- **Estado e datas:** Estado "Rascunho", criado e atualizado em 2026-11-22. O campo Revisores está vazio.
- **Data da medição:** escrevi "outubro de 2026" no lugar de "mês passado". É só o mês anterior à data de hoje, então corrija se a medição foi outra.
- **Riscos e rollout:** você não deu conteúdo para essas seções além da latência, então não inventei nada. Riscos traz só a latência de +5 ms, ainda não medida. Rollout só aponta para as perguntas.
- **Sem diagrama:** o fluxo está descrito em texto. Um diagrama pediria detalhes que você não deu, como a ordem entre gravar no Redis e publicar no Kafka.

As 8 perguntas abertas estão no final do doc. As mais importantes:
- **Falha do serviço ou do Redis:** o evento passa sem deduplicar ou é rejeitado?
- **Reenvio depois de 24h:** o que acontece, e por que a janela é de 24h?
- **Ordem de gravação:** a chave vai para o Redis antes ou depois de publicar no Kafka?
- **Rollout:** quais as fases, o critério de avanço e o de rollback?

As outras perguntas são sobre a origem da chave idempotente, a capacidade esperada e quem revisa o doc.
