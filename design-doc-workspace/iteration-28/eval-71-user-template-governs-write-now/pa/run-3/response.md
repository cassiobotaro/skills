Terminei o design doc e passei o unslop nele. Vou resumir o que ficou no arquivo.

O doc está em `docs/design/dedup-eventos.md`, com o estado Rascunho.

**Template.** Mantive as seções de `TEMPLATE.md`, na ordem do template: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.
- **Desvio:** o template não tem lugar para as alternativas que vocês discutiram nem para o trade-off aceito. Coloquei os dois como subseções de Proposta (`Alternativas consideradas` e `Trade-off aceito`), sem criar seção nova. A arquitetura pode preferir outro lugar para eles, então vale conferir.
- **Diagrama:** a Proposta tem um diagrama de sequência em Mermaid, com texto explicativo logo depois. Usei só os nomes que você deu (ingestor, serviço, Redis, Kafka).

**Números do doc.**
- 4% de duplicatas em outubro de 2026. Interpretei "mês passado" como outubro, já que hoje é 2026-11-22.
- Meta de duplicatas abaixo de 0,1%.
- Latência extra de +5 ms, marcada como estimativa, não como limite.

**Pontos que decidi sozinho:**
- **Numeração:** usei DD-2026-001, porque não há outros docs em `docs/design/`. Confirme se é o número certo.
- **Revisores:** deixei em branco.
- **Seções sem conteúdo:** Plano de rollout e as mitigações de dois riscos (Redis indisponível e reenvio após 24h) dizem "A definir", apontando para as perguntas. Você não disse nada sobre eles e não quis inventar.
- **Edições do unslop:**
  - Cortei uma frase que eu tinha escrito, dizendo que nenhum componente descarta repetidos hoje. Você não afirmou isso.
  - Tirei uma frase que dizia que o reenvio entre reinícios é um caso que vocês querem eliminar. Também não foi dita.
  - Corrigi "Os 24 horas" para "As 24 horas".

**Perguntas abertas.** São 10, no final do doc, em quatro grupos:
- **Rollout:** fases, critério de avanço e critério de rollback.
- **Falhas e riscos:** o que o serviço faz com o Redis fora do ar, se o Redis é dedicado e se tem alta disponibilidade, e se as 24h cobrem o maior intervalo de retry.
- **Chave e métricas:** quem gera a chave idempotente, se os 5 ms são um limite ou só estimativa, e como a taxa de duplicatas será medida.
- **Impacto e revisão:** quem revisa e quais outros times são afetados.

Não commitei nada.
