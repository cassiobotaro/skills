Salvei o documento em `docs/design/dd-2026-001-deduplicacao-de-eventos.md`, com as seções do template na ordem original: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas. Não rodei nenhum teste, porque é só documentação. Não renderizei o diagrama Mermaid, então vale conferir como ele aparece.

**O que ficou no documento**
- **Motivação:** os 4% de duplicatas em outubro de 2026 e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave guardada no Redis por 24h. Tem um diagrama de sequência seguido de texto. O texto registra também que um reenvio depois das 24h não seria reconhecido como duplicata.
- **Métricas:** duplicatas de 4% para menos de 0,1%.

**Desvio do template:** acrescentei a seção "Alternativas consideradas" entre Proposta e Riscos. O template não tem onde registrar as alternativas descartadas, o "não fazer nada" e o trade-off dos +5 ms, e o time de arquitetura vai querer ver isso. O resto do esqueleto está intacto. Se o time não aceitar seção extra, é só remover essa seção e levar o conteúdo para a Proposta.

**O que ficou como pergunta:** só escrevi o que você me disse. Plano de rollout está vazio, apontando para a pergunta 4. Em Riscos, só entrou a latência, e os demais riscos apontam para a pergunta 2. As perguntas no final do documento:
1. Quem são os revisores? O número DD-2026-001 também precisa de confirmação, porque `docs/design/` só tinha o template.
2. Quais são os riscos e as mitigações? Por exemplo, o que o serviço faz se o Redis cair, e o que acontece com a chave se a gravação no Kafka falhar.
3. De onde vem a chave idempotente: o produtor gera ou o serviço deriva do conteúdo?
4. Como é o rollout, com fases, critério de avanço e rollback?
5. Qual é o limite máximo de latência além dos +5 ms, e como medir?
6. Como medimos a taxa de duplicatas depois do lançamento?

Passei o unslop na prosa e cortei duas frases que afirmavam mais do que você tinha dito. Uma dizia que os consumidores passam a receber cada evento uma vez. A outra dizia que a latência "ainda não foi medida".

Não commitei nada.
