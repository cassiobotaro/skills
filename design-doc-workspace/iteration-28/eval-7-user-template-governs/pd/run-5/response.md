Salvei o doc em `docs/design/DD-2026-001-servico-deduplicacao-eventos.md`, com as seis seções do template na ordem. Ele está como Rascunho e tem muitos buracos.

**Desvios do template, para você aceitar ou não**
- **Alternativas:** o template não tem lugar para as alternativas que vocês descartaram. Criei a subseção "Alternativas consideradas" dentro de Proposta, com o motivo de cada descarte.
- **Número do doc:** `DD-2026-001` é um palpite, porque a pasta só tem o template. Ajuste se houver numeração em outro lugar.

**O que você deu e já está no doc**
- **Motivação:** os 4% de duplicatas, o impacto no faturamento e as duas reclamações do financeiro.
- **Proposta:** o fluxo com Redis e a janela de 24h.
- **Alternativas:** as duas que vocês descartaram.
- **Riscos:** o salto extra e a estimativa de +5ms.
- **Métricas de sucesso:** a meta de ficar abaixo de 0,1%.

**O que ficou como pergunta em aberto**
- **Riscos:** só o salto extra e o +5ms são seus. Não inventei outros. O que acontece se o Redis cair? E se a chave for gravada e a publicação no Kafka falhar? E se o reenvio chegar depois de 24h?
- **Rollout:** fases, critério de avanço e critério de rollback.
- **Desenho:** quem gera a chave idempotente e como ela é composta. Também falta a avaliação de "não fazer nada" como alternativa.
- **Métricas:** como medir a taxa de duplicatas depois do lançamento e qual o limite aceitável de latência.
- **Revisores:** quem são.

Não coloquei diagrama. Qualquer desenho do fluxo já teria que fixar a ordem entre gravar a chave e publicar, e essa ordem está em aberto.

Se você me responder essas perguntas, eu preencho Riscos e Rollout e tiro as pendências.
