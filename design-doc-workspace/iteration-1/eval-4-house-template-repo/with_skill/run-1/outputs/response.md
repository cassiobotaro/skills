Olhei o que já tem em `docs/design/` (só o `dd-2026-007-cache-de-catalogo.md`) e segui o mesmo padrão de vocês: título `DD-AAAA-NNN · ...`, cabeçalho em tabela chave-valor, e as seções Resumo / Contexto / Proposta (com `### Compensações` usando ✓/✗) / alternativas / Riscos (tabela) / Plano de entrega. Continuei a numeração: o doc novo é **DD-2026-008**.

Arquivo criado: `docs/design/dd-2026-008-rate-limiting-api-publica.md`

O que entrou, com base no que você passou do war room:

- **Proposta**: rate limit por token no Kong, janela deslizante com contadores no Redis de sessão, limites por plano (free 10 rps, pro 100 rps, enterprise negociado), `429` + `Retry-After`.
- **Compensações** explícitas: o trade-off aceito (cliente legítimo em pico pode tomar 429, mitigado com Retry-After + alerta pro time de contas) e o custo de colocar o Redis de sessão no caminho crítico.
- **Alternativas** em tabela, incluindo "não fazer nada": limitar dentro do serviço (tarde demais) e módulo pago gerenciado (custo + lock-in), ambos descartados.
- **Riscos**: só o real — Redis de sessão virar ponto de contenção, com a mitigação de medir antes (começando pelo shadow mode).
- **Plano de entrega** em fases: shadow mode → enforcing no free → enforcing geral.

Decisões que vale você revisar:

1. **O falso positivo de NAT eu deixei de fora dos riscos de propósito**, porque você mesmo disse que ele não existe (o limite é por token, não por IP). Em vez de virar risco, registrei "limite por IP" em *Fora de escopo*, explicando que NAT/IP compartilhado não influencia a contagem — assim fica claro pra quem ler depois por que isso não é problema.
2. Adicionei um **Glossário** (rps, janela deslizante, 429, Retry-After, shadow mode, token) que o DD-2026-007 não tinha — esse doc usa mais termos que um revisor de Contas/CS poderia tropeçar. Se preferir manter exatamente igual ao 007, é só remover.
3. Coloquei você (Cássio Botaro) como autor por padrão; ajusta se for outra pessoa.

O que eu não preenchi (precisa de você):

- **Revisores**: deixei "a definir" com sugestões (Plataforma/Gateway, SRE, Contas/Customer Success). Quem assina a revisão?
- **Critério de promoção entre as fases**: registrei como questão em aberto — qual o limiar (ex.: latência adicional aceitável no Redis) pra sair do shadow mode pro enforcing?
