Salvei o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Ele está no estado Rascunho, com você como autor e a data de hoje (2026-11-23). Como não havia outros docs na pasta, usei DD-2026-001.

Mantive as seis seções do template, na ordem dele. Duas seções têm lacunas porque você não deu o conteúdo e eu não quis inventar:

- **Riscos:** só consta a latência de +5 ms, que você aceitou. O resto aponta para Perguntas abertas.
- **Plano de rollout:** está vazio e aponta para Perguntas abertas. Faltam as fases, o critério de avanço e o de rollback.

Fiz um desvio do template. Ele não tem lugar para as alternativas que vocês discutiram, então coloquei "Alternativas consideradas" como subseção dentro de Proposta. Isso não muda as seções do template. Se o time de arquitetura for estrito, dá para tirar a subseção ou mover o conteúdo para outro lugar.

Para fechar as lacunas, preciso destas respostas, que também estão em Perguntas abertas:

1. Quem gera a chave idempotente e em que formato? O que acontece com um evento que chega sem chave?
2. Quais outros riscos existem, em especial o que o serviço faz quando o Redis cai? Qual a mitigação de cada um?
3. Como será o rollout, com fases, critério para avançar e critério de rollback?
4. Como vamos medir a taxa de duplicatas e a latência para comparar com os 4% e a meta de 0,1%?
5. Quem são os revisores? Esse campo ficou em branco no cabeçalho.

Se você me passar essas respostas, eu preencho as seções e tiro as perguntas correspondentes.
