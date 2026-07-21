Escrevi o doc em `docs/design/dd-2026-008-rate-limiting-api-publica.md`, seguindo o padrão do DD-2026-007: mesma tabela de cabeçalho, e as seções **Resumo → Contexto → Proposta → Compensações (✓/✗) → Riscos (tabela) → Plano de entrega**, na mesma ordem e em português.

Duas seções a mais que o DD-2026-007 não tem, porque você me deu a substância e ela não caberia honestamente nas outras:

- **Objetivos** — o "nenhum token excede seu limite por mais de 1s" e o "aguentar um cliente abusivo sem degradar os demais" são metas verificáveis; enfiá-las no Resumo ou no Contexto tiraria delas o caráter de critério de sucesso.
- **Alternativas consideradas** — as duas opções descartadas no war room (limitar dentro de cada serviço; módulo pago do gateway gerenciado) são o que dá valor ao doc daqui a um ano. Incluí também o "não fazer nada", com o INC-4412 como razão de descarte.

Se o padrão da casa for fechado nas seis seções do DD-2026-007, é só me dizer que eu dobro as duas para dentro do Resumo e da Proposta.

Outras decisões que vale você conferir:

- **O falso positivo de NAT compartilhado ficou de fora.** Você disse que ele não existe, já que o limite é por token e não por IP — então ele não entra nem como risco nem como compensação. Um risco que não existe no desenho envelhece mal.
- **Diagramas.** O DD-2026-007 não tem nenhum, mas o desenho aqui tem três peças e dois caminhos de resposta, então incluí um diagrama de contêineres (C4, renderizado em `docs/design/diagrams/dd-2026-008-arquitetura.png`, com a fonte Structurizr dobrada num `<details>`) e um diagrama de sequência Mermaid do caminho da requisição. Ambos validados. Se preferir manter o padrão sem diagramas, eu removo.
- **Riscos** ficou com uma linha só (o Redis de sessão virar ponto de contenção, com a medição no shadow mode como mitigação) — foi o único que você levantou.

Faltam quatro coisas que só você pode responder:

1. **Autores e revisores** — deixei "A definir" no cabeçalho. Quem assina, e quais áreas revisam? Pelo desenho, sugiro alguém de SRE (o Redis no caminho crítico de tudo) e alguém de Contas/Customer Success (é o time que vai avisar os enterprise no pico).
2. **A medição do Redis** — o shadow mode mede o quê, exatamente, e a partir de que número vocês desistem de usar o Redis de sessão? Um limiar escrito transforma o risco em decisão; sem ele, "vamos medir antes" fica sem critério de parada.
3. **Quanto tempo em cada fase**, e existe rollback? Se o enforcing no free der errado, dá para voltar ao shadow mode por configuração ou precisa de deploy?
4. **O `Retry-After` vale quanto?** Um valor fixo ou o tempo que falta para a janela liberar? Isso muda o comportamento do cliente legítimo em pico, que é justamente a compensação que vocês aceitaram.

Uma sugestão para depois: o doc usa rps, 429, `Retry-After`, janela deslizante e shadow mode. Se ele for circular fora da engenharia — Contas, por exemplo —, um glossário curto logo depois do cabeçalho paga o espaço que ocupa. Como o DD-2026-007 não tem essa seção, não adicionei por conta própria.
