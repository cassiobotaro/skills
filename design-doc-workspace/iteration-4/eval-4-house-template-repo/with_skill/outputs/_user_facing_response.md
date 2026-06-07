Pronto. Segui o padrão de `docs/design/` (mesma estrutura do DD-2026-007: tabela de metadados, Resumo, Contexto, Proposta com Compensações em ✓/✗, Riscos em tabela e Plano de entrega em fases) e escrevi o doc novo:

**`docs/design/dd-2026-008-rate-limiting-api-publica.md`** — estado **Proposto** (ainda sem revisores; me diga quem revisa que eu preencho).

O que entrou:

- **Contexto** ancorado no INC-4412 (40x de tráfego, API derrubada por 25 min, nenhum limite por cliente hoje).
- **Proposta**: rate limit por token no Kong, janela deslizante com contadores no Redis de sessão que já usamos, limites por plano (free 10 rps, pro 100 rps, enterprise negociado) e `429` + `Retry-After`. Inclui um diagrama de sequência do fluxo da requisição, seguido de texto explicando por que a decisão fica no gateway (barrar o abuso antes da malha).
- **Compensações** com o trade-off aceito explícito: cliente legítimo em pico (Black Friday) pode tomar `429`, mitigado pelo `Retry-After` e pelo alerta para o time de contas avisar os enterprise.
- **Alternativas consideradas** em tabela, incluindo "não fazer nada", limitar dentro de cada serviço (tarde demais — já consumiu gateway e malha) e o módulo pago gerenciado (custo + lock-in).
- **Objetivos** mensuráveis: nenhum token excede o limite por mais de 1s; a API aguenta um cliente abusivo sem degradar os demais.
- **Riscos**: o Redis de sessão virar ponto de contenção, com a mitigação de medir antes (é para isso que serve a fase de shadow mode).
- **Plano de entrega** em três fases: shadow mode (só medindo) → enforcing no free → enforcing geral.

Duas observações:

1. **Não incluí o falso positivo de NAT/IP compartilhado** — como você mesmo notou, ele não se aplica aqui, já que o limite é por token e não por IP. Registrar isso só confundiria o leitor.
2. O servidor de validação do Mermaid estava fora no momento, então o diagrama de sequência **não foi validado por máquina** — é sintaxe padrão e renderiza no GitHub/GitLab, mas vale uma conferida visual no preview.

Quer que eu já preencha os revisores e mude o estado para "Em revisão"?
