Salvei o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Ele segue o `TEMPLATE.md`: mesmo cabeçalho e as seis seções na ordem do template. Não comitei.

**Uma escolha de estrutura para você conferir:** o template não tem lugar para alternativas nem para o custo aceito. Coloquei os dois como subseções dentro de **Proposta**, em vez de criar seções novas, para não mexer no esqueleto que a arquitetura cobra. Se eles preferirem outro lugar, é só mover.

**O que entrou, só com o que você me passou:**
- **Motivação:** os 4% de duplicatas vindos de retry, os relatórios de faturamento inflados e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka com a chave no Redis por 24h, mais um diagrama de sequência em Mermaid. Também traz o +5ms estimado como custo e a tabela de alternativas: não fazer nada, deduplicar no consumidor e a idempotência nativa do produtor Kafka.
- **Métricas de sucesso:** de 4% para abaixo de 0,1%.

**O que ficou incompleto:** em **Riscos** está só a latência, e a mitigação não foi definida. **Plano de rollout** está vazio. As duas seções apontam para as perguntas abertas. Não inventei riscos nem fases.

**Perguntas abertas no fim do doc (9):**
1. Quem são os revisores.
2. De onde vem a chave idempotente.
3. Por que a janela é de 24h.
4. Em que ordem o serviço grava no Redis e publica no Kafka, e o que acontece quando uma das duas falha.
5. Que outros riscos existem e como mitigar cada um.
6. Como chegaram nos 5ms e qual o teto de latência aceitável.
7. Como será o rollout, com critérios de avanço e de rollback.
8. Como os 4% foram medidos.
9. O que fica fora do escopo.

O doc fica em **Rascunho** até essas respostas entrarem. As perguntas 4, 5 e 7 devem ser as primeiras que a arquitetura vai cobrar.
