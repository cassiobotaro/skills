Terminei de escrever o doc e passei o unslop. Falta só te dar o resumo.

O doc está em `docs/design/dd-2026-008-rate-limiting-api-publica.md`, com estado Rascunho. Segui o esqueleto do DD-2026-007: cabeçalho, Resumo, Contexto, Proposta com Compensações (✓/✗), Riscos e Plano de entrega.

Acrescentei três seções que o padrão não tem, porque o conteúdo não tinha onde entrar: **Objetivos**, **Alternativas consideradas** (inclui "não fazer nada", com o INC-4412 como motivo) e **Perguntas em aberto**. Se preferir, dá pra dobrar Objetivos dentro de Contexto ou Proposta.

Decisões de redação:
- **Data do incidente:** escrevi 2026-11-21 (você disse "ontem" e hoje é 2026-11-22).
- **NAT compartilhado:** não está nos riscos, porque você disse que não se aplica. Só aparece na Proposta, como a nota de que o limite é por token, não por IP.
- **Compensações:** não coloquei como benefício que "o cliente abusivo só afeta a si mesmo", porque isso é o objetivo, não algo medido.

O que eu não inventei e ficou em aberto:
- **Autores e revisores:** estão como "A definir". Sugeri Plataforma, SRE e o time de contas.
- **Redis fora do ar:** não sei se o gateway deixa passar ou bloqueia.
- **Critérios e prazos das fases:** não há critério para sair do shadow mode nem duração de cada fase.
- **Contenção no Redis:** falta o limite de carga que indica que ele virou ponto de contenção.
- **Alerta ao time de contas:** falta a condição que o dispara, o primeiro 429 ou a aproximação do limite.
- **Fora de escopo:** não ficou nada definido.

Me passa essas respostas que eu fecho o doc.
