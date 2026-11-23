Escrevi o design doc em `docs/design/deduplicacao-de-eventos.md`, com as seções do template na ordem original. Não commitei nada.

- **Alternativas e trade-off:** o template não tem seção para isso. Pus as duas alternativas descartadas e o trade-off dos +5ms como subseções (`###`) dentro de Proposta. Assim as seções de nível 1 ficam idênticas às do template, que o time de arquitetura exige. Se preferirem seções próprias, é só promover os títulos.
- **Diagrama:** Proposta tem um diagrama de sequência em Mermaid (ingestor, serviço, Redis, Kafka), seguido do texto explicativo. Não pus tecnologia nem protocolo nas setas, porque você não os informou.
- **Seções sem conteúdo seu:** Riscos (só entrou a latência, que você aceitou), Plano de rollout e a forma de medir as métricas apontam para as Perguntas abertas. Não inventei nada para preenchê-las.
- **Número do documento:** usei `DD-2026-001`, só porque não há outros docs na pasta. Confirme com o time de arquitetura.
- **Revisores:** o campo está vazio.

As 12 perguntas abertas estão no fim do documento. As que mais pesam são:
- De onde vem a chave idempotente, e quem a gera.
- O que o serviço faz se o Redis cair (deixa passar ou bloqueia).
- Por que 24h, e o que acontece com um reenvio depois da janela.
- Se os +5ms foram medidos ou são projeção.
- Como medimos a taxa de duplicatas.
- Quais times são afetados e quem opera o serviço.
- Se "não fazer nada" foi considerado como alternativa.

Rascunho, datado de 2026-11-23, autor Rafael Nunes.
