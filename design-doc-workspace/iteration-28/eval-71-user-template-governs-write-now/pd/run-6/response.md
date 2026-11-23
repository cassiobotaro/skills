Escrevi o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Não commitei nada.

Segui as seis seções do template, na ordem. Não criei seção nova. Alternativas e trade-off ficaram como subseções de Proposta, e a meta de 0,1% ficou em Métricas de sucesso.

- **Diagrama:** pus um diagrama de sequência em Mermaid (ingestor → serviço → Redis → Kafka), seguido de texto. Deixei de fora tecnologias e protocolos que você não citou.
- **Número do documento:** usei DD-2026-001 porque `docs/design/` só tinha o template. Confirme ou corrija.
- **Revisores:** o campo ficou vazio.
- **Riscos:** só registrei a latência de +5 ms, que você já tinha aceitado. Não inventei outros riscos.
- **Plano de rollout:** ficou como "ainda não definido", com remissão às perguntas.
- **Perguntas abertas:** são 14, agrupadas por seção. As que mais pesam:
  - O que acontece com a ingestão se o Redis ou o serviço cair?
  - Se o serviço grava a chave no Redis e falha antes de publicar no Kafka, o reenvio do produtor é descartado e o evento se perde. Como evitamos isso?
  - Quais são as fases, os critérios de avanço e o rollback do rollout?
  - Como medimos a taxa de duplicatas?
  - Qual é o limite aceitável de latência?
  - Reenvios que chegam depois da janela de 24h ficam sem deduplicação. Isso é aceitável?
