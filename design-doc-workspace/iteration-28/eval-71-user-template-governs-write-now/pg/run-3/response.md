Escrevi o doc em `docs/design/deduplicacao-de-eventos.md`. Ele usa as seções do template, na ordem, com ID DD-2026-001 (era o primeiro doc da pasta). Estado: Rascunho, criado em 2026-11-23, com você como autor.

- **Seção extra:** acrescentei "Alternativas consideradas" depois de Proposta. O template não tem lugar para as duas alternativas que vocês descartaram, e o texto da seção avisa isso. Se a arquitetura não aceitar seção fora do template, mova esse conteúdo para dentro de Proposta.
- **Meta de 0,1%:** ela ficou em Métricas de sucesso, ao lado da linha de base de 4%.
- **Riscos:** só a latência de +5ms está registrada, porque foi o único risco que você citou. Não inventei os outros.
- **Plano de rollout:** não tenho nada seu sobre esta seção. Ela só aponta para as perguntas abertas.
- **Perguntas abertas:** são 10, agrupadas por Riscos, Rollout, Métricas e Documento. As principais:
  - O que acontece com a ingestão se o Redis cair?
  - O que acontece se o serviço falhar depois de gravar a chave e antes de entregar ao Kafka?
  - Quem gera a chave idempotente?
  - Qual é o critério de rollback?
  - Quais são os revisores?
- **Diagrama:** não incluí. Um diagrama exigiria detalhes que você não deu, como o comportamento em falha e os protocolos.

Quando você responder às perguntas, eu movo cada resposta para a seção certa e tiro a pergunta de Perguntas abertas.
