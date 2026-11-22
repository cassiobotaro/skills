Rafael, salvei o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`, seguindo as seis seções do `TEMPLATE.md` na ordem e com o cabeçalho completo. Duas seções ficaram sem conteúdo, esperando você. Não rodei o `unslop` nem uma revisão de typos.

**O que já está preenchido**
- **Motivação:** os 4% de duplicatas, o impacto no faturamento e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave idempotente guardada no Redis por 24h. O trade-off aceito, os +5ms de latência, está numa subseção.
- **Métricas de sucesso:** duplicatas abaixo de 0,1%.

**Desvio do template, para você aceitar ou não:** o template não tem lugar para as alternativas que você descreveu. Criei "Alternativas consideradas" dentro de Proposta, com três itens. Os dois descartes são os seus, e "não fazer nada" está pelo motivo que você já deu, a dor atual. O resto do esqueleto ficou intacto.

**O que ficou aguardando você**

Não inventei riscos nem rollout. Riscos e Plano de rollout trazem uma linha que aponta para as perguntas abertas. Preciso destas respostas:
1. **Riscos:** o que pode dar errado e como mitigar cada ponto?
2. **Plano de rollout:** quais fases, qual critério de avanço e qual de rollback?
3. **Métricas:** além da taxa de duplicatas, quer acompanhar latência ou disponibilidade, e com qual limite?
4. **Revisores:** quem deve revisar? O campo ficou vazio.
5. **Numeração:** `docs/design/` não tinha outros docs, então usei DD-2026-001. Confirme se é o número certo.

Me passe as respostas e eu preencho as seções.
