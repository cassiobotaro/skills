Salvei o doc em `docs/design/DD-2026-001-servico-de-deduplicacao-de-eventos.md`. Usei o ID 001 porque a pasta só tinha o template. Segui as seções do template na ordem: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.

- **Desvio do template:** ele não tem lugar para as alternativas, e elas são o centro do trade-off. Acrescentei "Alternativas consideradas" como subseção dentro de Proposta e avisei isso no próprio texto. Se a arquitetura não aceitar subseção extra, é só mover ou tirar.
- **Diagrama:** fiz um diagrama de sequência em Mermaid do fluxo produtor, ingestor, serviço, Redis e Kafka, seguido de texto. Não coloquei protocolos nem tecnologias que você não citou.
- **Riscos e rollout:** você só deu o risco da latência (+5ms), e deixei esse como risco declarado. Não inventei fases, critérios de avanço nem rollback. A seção de rollout diz que está indefinida e aponta para as perguntas.
- **Perguntas abertas:**
  - A chave idempotente: qual é e quem a gera.
  - O comportamento quando o Redis cai.
  - Concorrência entre dois reenvios simultâneos.
  - Dimensionamento do Redis e risco de perder chaves.
  - Por que 24h.
  - Como medir os 4% e os 0,1%.
  - Se o +5ms foi medido ou só estimado.
  - Fases de rollout e rollback.
  - Quais times são impactados e quem revisa.
- **Campos em branco:** deixei os Revisores vazios e usei a data de hoje (2026-11-23) em criação e atualização.

Não rodei a skill `unslop` porque ela não está instalada aqui.
