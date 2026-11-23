Salvei o doc em `docs/design/deduplicacao-de-eventos.md`, seguindo as seções do TEMPLATE.md na ordem: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas. Não rodei revisão de prosa (o skill `unslop` não está instalado) nem renderizei o diagrama.

**Desvios do template**
- Acrescentei "Alternativas consideradas" como subseção da Proposta, porque o template não tem lugar para as duas opções descartadas. O doc diz isso explicitamente. Se a arquitetura não aceitar, é só mover o conteúdo.
- Incluí um diagrama de sequência em Mermaid com o fluxo produtor → ingestor → dedup → Redis → Kafka, seguido de texto explicando.

**O que ficou fora**
- O plano de rollout é só um aviso de que ainda não está definido, porque você não deu nada sobre ele.
- Os riscos se resumem aos +5ms de latência, que você aceitou. A estimativa de +5ms ainda não foi medida e o doc diz isso.
- Revisores ficou em branco.
- O ID DD-2026-001 é escolha minha, porque a pasta só tinha o template.

**Perguntas no final do doc (10)**
- **Indisponibilidade do Redis:** o que acontece com a ingestão, fail-open ou fail-closed?
- **Ponto único de falha:** o serviço é ponto único de falha?
- **Janela de 24h:** ela é suficiente para os reenvios dos produtores?
- **Ordem registrar × publicar:** se a chave é gravada e a publicação no Kafka falha, o reenvio seguinte é descartado e o evento se perde. Qual é a ordem entre registrar a chave e publicar?
- **Chave idempotente:** quem a define, o produtor ou o ingestor? Todos os produtores já enviam uma?
- **Volume de eventos:** quantos eventos por segundo e quantas chaves em 24h?
- **Protocolos:** quais ligam os componentes? Deixei fora do diagrama.
- **Rollout:** como é, e qual o critério de avanço e de rollback?
- **Latência:** qual o limite aceitável além dos +5ms, e como medir latência e taxa de duplicatas em produção?
- **Revisores e ID:** quem revisa, e o ID está certo?
