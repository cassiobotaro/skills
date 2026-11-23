Salvei o doc em `docs/design/dedup-de-eventos.md`, seguindo o TEMPLATE.md na ordem: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas. Usei só o que você me disse e não rodei nenhuma checagem do doc.

**Desvios do template**
- **Seção extra:** acrescentei "Alternativas consideradas" como subseção de Proposta. As duas alternativas descartadas e o "não fazer nada" não tinham outro lugar no template. Se a arquitetura só aceita as seções exatas, é só mover o conteúdo para dentro da Proposta.
- **Número do documento:** usei DD-2026-001, porque não há outros docs na pasta. Ajuste se a numeração já existe em outro lugar.

**O que está no doc**
- **Datas e estado:** estado Rascunho, datas de hoje (2026-11-23) e você como autor.
- **Risco:** a latência de +5ms aparece como risco aceito. Registrei que é uma estimativa, não uma medida.
- **Métricas:** os 4% de duplicatas hoje e a meta abaixo de 0,1%.

**O que ficou como pergunta**
- **Riscos e rollout:** você não deu nada além da latência para Riscos nem para o Plano de rollout. As duas seções só apontam para as Perguntas abertas, sem texto que eu tenha inventado.
- **Perguntas no final:** são 10, incluindo a composição da chave idempotente, o que acontece se o Redis cair, a atomicidade entre gravar a chave e entregar ao Kafka, o plano de rollout e a lista de revisores.
- **Revisores:** o campo ficou "A definir".

Não incluí diagrama, porque a notação pediria detalhes (protocolos, tecnologias de cada caixa) que você não deu. Posso acrescentar um quando você responder às perguntas.
