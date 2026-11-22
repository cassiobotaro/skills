Salvei o design doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Não rodei nenhum teste nem renderizei o diagrama.

O documento segue as seções do `TEMPLATE.md`, na ordem do template. Está em estado Rascunho, com datas de 2026-11-22 e você como autor.

**O que entrou com o que você disse**
- A motivação traz os 4% de duplicatas, as duas reclamações do financeiro e a meta de ficar abaixo de 0,1%.
- A proposta descreve o serviço entre o ingestor e o Kafka, a chave guardada no Redis por 24h e o descarte dos repetidos. Tem um diagrama de sequência em Mermaid, sem protocolos nas setas, porque você não os citou.
- O custo de +5 ms no caminho crítico aparece em Riscos como trade-off aceito, marcado como estimativa não medida.

**Desvio do template, para você aceitar ou não**
- Acrescentei a seção "Alternativas consideradas" entre Proposta e Riscos. O template não tem lugar para elas, e é nelas que entram "não fazer nada", deduplicar no consumidor e a idempotência nativa do produtor Kafka. O documento explica o desvio. Se o time de arquitetura não aceitar seção extra, é só mover esse conteúdo para dentro de Proposta.

**O que ficou sem conteúdo**
- Plano de rollout e riscos além da latência ficaram só com uma frase apontando para Perguntas abertas, porque você não deu essa substância e eu não quis inventar.
- Perguntas abertas tem 14 perguntas, agrupadas por tema, e nenhuma está afirmada no corpo como fato. As mais importantes:
  - o comportamento se o Redis cair (fail-open ou fail-closed);
  - quem gera a chave idempotente;
  - por que 24h;
  - as fases e os critérios de rollback;
  - como medir a taxa de duplicatas depois.
- Os revisores ficaram em branco.
- O número `001` é provisório, porque não há outros docs no repositório. Confirme qual é o número certo.

Passei as revisões de redação (`technical-writing` e `unslop`) no texto que escrevi, sem mexer em títulos, no cabeçalho nem no diagrama.
