Salvei o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Não rodei validador nem linter, porque o repositório só tem o template.

- **Template:** mantive as seis seções na ordem original e o cabeçalho com o ID `DD-2026-001`. Usei `001` porque `docs/design/` só tinha o `TEMPLATE.md`. Se a numeração é global em outro lugar, ajuste.
- **Desvio do template:** o template não tem seção para alternativas nem para o trade-off aceito. Coloquei os dois como subseções dentro de **Proposta** (alternativas descartadas e os +5 ms de latência), sem criar seção nova. Se a arquitetura for rígida nisso, é fácil mover.
- **Preenchido com o que você disse:** a motivação com os 4% (como outubro de 2026) e as reclamações do financeiro, o fluxo ingestor → serviço → Redis (24h) → Kafka com um diagrama simples e a meta de 0,1%.
- **Não preenchido por falta de informação:**
  - O plano de rollout está sem conteúdo e remete às perguntas abertas.
  - Em Riscos, só consta a latência.
  - O campo Revisores ficou vazio.
- **Perguntas abertas (10):**
  - Quem gera a chave idempotente.
  - A ordem entre registrar no Redis e publicar no Kafka (se o Kafka falhar depois do registro, o reenvio seria descartado e o evento se perderia).
  - O que fazer se o Redis ou o serviço caírem.
  - O orçamento de latência.
  - Como medir a taxa de duplicatas.
  - O plano de rollout.
  - A capacidade do Redis.
  - Se manter o cenário atual foi avaliado como alternativa.
  - Quem revisa o doc.

Os riscos de indisponibilidade e de perda de evento são o que o time de arquitetura mais deve cobrar. Vale responder essas perguntas antes de submeter.
