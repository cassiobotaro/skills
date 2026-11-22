Escrevi o design doc e passei o `unslop` na prosa. Ele está em `docs/design/deduplicacao-de-eventos.md`, com as seções do `TEMPLATE.md` na ordem original. Não rodei nenhuma ferramenta para validar o Mermaid nem para conferir a renderização.

- **Seção extra:** o template não tem lugar para as alternativas que vocês discutiram. Criei "Alternativas consideradas" e "Trade-off aceito" como subseções de Proposta, e o doc avisa que elas não vêm do template. Se a arquitetura só aceita o formato exato, mova esse conteúdo para onde preferirem ou remova.
- **Conteúdo:** Motivação traz os 4% e as duas reclamações do financeiro. Proposta traz um diagrama de sequência em Mermaid, seguido de texto. As alternativas são consumidor, idempotência nativa do Kafka e manter o cenário atual. O trade-off aceito é o +5ms. As métricas são a meta de 0,1% e a latência estimada.
- **Diagrama:** não fixei a ordem entre guardar a chave e publicar no Kafka, nem pus protocolos nas setas, porque você não definiu nada disso.
- **Lacunas:** em Riscos, só escrevi os riscos que decorrem do que você disse (latência, Redis como dependência, janela de 24h). As mitigações ficaram "pendentes". O Plano de rollout ficou "ainda não definido". Não inventei fases nem critérios.
- **Número do documento:** `DD-2026-001` é um palpite, porque `docs/design/` só tinha o template. Confirme se o número está certo.
- **Revisores:** o campo está em branco.

As 13 perguntas ficaram em "Perguntas abertas". As que mais pesam são:
- Quem gera a chave idempotente.
- Se o serviço guarda a chave antes ou depois de publicar no Kafka.
- O que ele faz quando o Redis está fora.
- Por que 24h.
- Como será o rollout e se há um modo de observação antes de ligar o descarte.
- Como a meta de 0,1% será medida.

Não fiz commit.
