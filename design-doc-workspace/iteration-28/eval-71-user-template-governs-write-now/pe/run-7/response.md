Escrevi o doc em `docs/design/DD-2026-001-servico-deduplicacao-eventos.md`, com estado Rascunho. Não rodei o `unslop` nem uma revisão ortográfica à parte.

O doc segue as seções do template na ordem, com uma exceção: acrescentei **Alternativas consideradas**, entre Proposta e Riscos. O template não tem lugar para as duas alternativas que vocês descartaram, e o time de arquitetura vai querer ver o raciocínio. Se o formato rígido não admitir seção extra, é só mover o conteúdo para dentro de Proposta.

Só usei o que você me disse:
- **Motivação:** os 4% de duplicatas no mês passado e as duas reclamações do financeiro.
- **Proposta:** o fluxo ingestor → serviço → Kafka, com o Redis guardando a chave por 24h.
- **Riscos:** só a latência de +5ms, registrada como custo aceito.
- **Métricas de sucesso:** duplicatas abaixo de 0,1%.

O DD-2026-001 é o primeiro doc da pasta, então escolhi a numeração. O campo Revisores está vazio. Não fiz diagrama C4 nem de sequência, porque o fluxo cabe num esquema de texto e eu teria que inventar tecnologias e protocolos.

Há seções que você não cobriu. Em vez de inventar o conteúdo, deixei as lacunas em **Perguntas abertas**:
1. Quem revisa o doc.
2. Quem gera a chave idempotente e de que campos ela é composta.
3. Por que 24h, e se algum retry reenvia depois disso.
4. O que o serviço faz se o Redis cair, e se há outros riscos além da latência.
5. Se os +5ms vêm de medição ou de estimativa, e qual limite de latência inviabiliza a proposta.
6. O plano de rollout inteiro: fases, critério de avanço e de rollback. A seção está só com um ponteiro para cá.
7. Como medir a taxa de duplicatas, e em que prazo bater a meta.
8. Se existiu a alternativa "não fazer nada" e por que perdeu.
