Salvei o doc em `docs/design/deduplicacao-de-eventos.md`, seguindo o `TEMPLATE.md` na mesma ordem de seções. Não rodei revisão de estilo nem a checagem final de typos.

Só usei o que você me disse: os 4% de duplicatas, as duas reclamações do financeiro, o serviço com Redis e TTL de 24h, as duas alternativas descartadas, os +5ms e a meta de 0,1%. O estado ficou como Rascunho e as datas são de hoje, 2026-11-23.

Fiz três coisas fora do que o template prevê ou pede:
- **Alternativas e trade-off:** o template não tem seção para eles, então ficaram como subseções dentro de Proposta. Incluí também a alternativa "não fazer nada". Se a arquitetura preferir outro lugar, é só mover.
- **Diagrama:** coloquei um diagrama de sequência em Mermaid, sem nenhuma tecnologia além das que você citou.
- **Riscos:** listei só os que decorrem direto do desenho (os +5ms, o Redis como nova dependência no caminho crítico, a janela de 24h). As mitigações ficaram em aberto.

O número do documento ficou como `DD-2026-<seq>`, porque não há outros docs na pasta para continuar a numeração. O campo Revisores está vazio.

O Plano de rollout está marcado como "ainda não definido", porque você não deu nada sobre fases ou rollback.

No final do doc há 13 perguntas abertas. As mais importantes são:
- como a chave idempotente é formada;
- o que acontece se o Redis cair (deixar passar ou bloquear a ingestão);
- como evitar perder um evento se a chave for gravada e o Kafka falhar;
- o que responder ao produtor quando o evento é descartado;
- o volume de eventos e o dimensionamento do Redis;
- o plano de rollout.

Quando você responder, atualizo o doc.
