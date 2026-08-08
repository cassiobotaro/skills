Li o `docs/design/dd-2026-007-cache-de-catalogo.md` e segui o padrão da casa: título `DD-<ano>-<seq> · <assunto>`, tabela de cabeçalho, **Resumo → Contexto → Proposta (com ### Compensações) → Riscos (tabela) → Plano de entrega**.

Criei `docs/design/dd-2026-008-rate-limiting-api-publica.md` (continuei a numeração a partir do DD-2026-007).

**Saí um pouco do padrão, e quero seu aval:** você me deu duas coisas que o modelo da casa não tem onde guardar, e preferi registrar a perder:

- **Objetivos** — o "nenhum token excede o limite por mais de 1s" e o "aguentar um cliente abusivo sem degradar os demais" ficariam sem lugar.
- **Alternativas consideradas** — limitar dentro de cada serviço, o módulo pago do gateway gerenciado e o não fazer nada, cada uma com o motivo do descarte. É o que faz a decisão continuar auditável daqui a um ano.

Se você preferir manter o esqueleto do DD-2026-007 estrito, eu dobro as duas dentro de Contexto e Proposta.

**Uma coisa que deixei de fora de propósito:** o falso positivo com NAT compartilhado. Como você mesmo disse, ele não existe — o limite é por token, não por IP. Registrar um risco inexistente só faria o revisor discutir um problema que não temos.

**Perguntas para fechar o documento:**

1. **Autores e revisores** — deixei os dois campos como _a definir_. Quem assina? E quais áreas revisam? Pelo que o desenho toca, eu sugeriria alguém de Plataforma/Gateway (Kong) e de SRE (o Redis de sessão no caminho crítico).
2. **Estado** — coloquei `Rascunho`. Se o war room já vale como aprovação da proposta, mudo para `Aprovado` como no DD-2026-007.
3. **Riscos** — a tabela está com uma linha só (contenção no Redis de sessão). Saiu mais alguma coisa do war room, ou esse foi mesmo o único levantado?
4. **Shadow mode** — qual número vocês vão olhar nessa fase para decidir que dá para ligar o enforcing? É o que amarra a medição do Redis ao objetivo de 1s, e hoje o plano de entrega só diz "medindo".
5. **Limite enterprise** — "negociado" fica registrado onde (contrato, config do Kong, planilha)? Quem operar precisa saber onde olhar.

Me responde o que quiser e eu já aplico no arquivo.
