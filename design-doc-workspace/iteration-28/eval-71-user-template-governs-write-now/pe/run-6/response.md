Salvei o doc em `docs/design/dd-2026-001-deduplicacao-de-eventos.md`, seguindo as seções do `TEMPLATE.md` na ordem original. Não commitei nada.

- **O que está escrito:** a motivação (4% de duplicatas em outubro de 2026, financeiro reclamando duas vezes), a proposta com um diagrama de sequência, o trade-off dos +5 ms e a meta de duplicatas abaixo de 0,1%. O estado é Rascunho e o autor é você.
- **Desvio do template:** ele não tem lugar para as alternativas que vocês discutiram. Coloquei a subseção "Alternativas consideradas" dentro de Proposta, sem mexer no esqueleto. Se a arquitetura for rígida nisso, é só mover o conteúdo.
- **Seções com pouco conteúdo:** só o +5 ms entrou em Riscos, sem mitigação, e Plano de rollout só aponta para as perguntas abertas. Não inventei nada que você não tenha dito.
- **Diagrama:** deixei sem protocolos e sem tecnologia nas setas e caixas, porque você não os informou. O Redis aparece só como Redis.
- **Número do documento:** usei DD-2026-001 porque a pasta só tinha o template. Confirme se é o próximo da sequência.
- **Campo Revisores:** ficou em branco.

As **Perguntas abertas** no fim do doc são estas:
1. Fases, critério de avanço e rollback.
2. Comportamento quando o Redis falha.
3. Teto de latência e quem mede.
4. Como medir o percentual de duplicatas.
5. Por que a janela é de 24 horas.
6. Quem gera a chave idempotente.
7. Se "não fazer nada" foi considerado.
8. Times impactados além do financeiro.
9. Revisores e numeração.
