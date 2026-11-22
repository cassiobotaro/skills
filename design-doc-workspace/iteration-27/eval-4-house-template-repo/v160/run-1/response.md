Escrevi o doc em `docs/design/dd-2026-008-rate-limiting-api-publica.md`. Está como Rascunho, com Autores e Revisores em aberto.

Segui o padrão do DD-2026-007, que é o único doc que existe lá: cabeçalho em tabela, Resumo, Contexto, Proposta com Compensações (✓/✗), Riscos em tabela e Plano de entrega. Continuei a numeração com o ID 008.

Duas coisas fogem do padrão. Acrescentei **Objetivos**, porque o 007 não tem onde pôr a meta de 1s e a de não degradar os outros clientes. Também coloquei **Alternativas consideradas** dentro da Proposta, com "não fazer nada" incluída, e uma seção **Questões em aberto** no fim. Se preferir o esqueleto idêntico ao 007, é só mover ou remover.

Deixei vários pontos em aberto em vez de inventar. Estão todos na seção Questões em aberto:
- Autores e revisores (sugiro Plataforma, SRE e o time de contas).
- Prazo de cada fase e critério para passar da shadow mode para o enforcing.
- O que o Kong faz se o Redis cair: deixa passar ou rejeita?
- O que fica fora do escopo.
- Como e com qual métrica medir a carga no Redis antes do enforcing.

O falso positivo com NAT compartilhado ficou de fora, como você disse. Pelo mesmo motivo, não escrevi nada sobre o risco inverso, de um cliente com um token só usado em muitos hosts.

Escrevi a data do incidente como 2026-11-21, a partir do seu "ontem". Corrija se não for isso.

Depois de escrever, passei o unslop no texto. Ele só cortou uma frase de enchimento.
