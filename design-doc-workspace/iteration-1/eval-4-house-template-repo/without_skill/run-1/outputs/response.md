Olhei o que tem em `docs/design/` (só o `dd-2026-007-cache-de-catalogo.md`) e segui o mesmo padrão: título `# DD-AAAA-NNN · Tema`, tabela de metadados, e as seções Resumo / Contexto / Proposta (com **Compensações** usando ✓/✗) / Riscos (tabela Risco | Mitigação) / Plano de entrega.

Criei o doc novo em:

`docs/design/dd-2026-008-rate-limiting-api-publica.md`

O que coloquei:

- **Contexto:** INC-4412, os 40x de tráfego, os 25 min de indisponibilidade e o fato de hoje não haver limite por cliente.
- **Proposta:** rate limit por token no Kong, janela deslizante com contadores no Redis de sessão, limites por plano (free 10 rps / pro 100 rps / enterprise negociado) e 429 com `Retry-After`.
- **Alternativas:** limitar dentro do serviço (descartada — tarde demais) e o módulo pago do gateway gerenciado (descartado — custo e lock-in).
- **Compensações:** o trade-off do cliente legítimo em pico (Black Friday) tomar 429, mitigado pelo `Retry-After` e pelo alerta ao time de contas.
- **Riscos:** o Redis de sessão virar ponto de contenção, com a mitigação de medir antes (no shadow mode).
- **Objetivos:** nenhum token excede o limite por mais de 1s e a API aguenta um cliente abusivo sem degradar os demais.
- **Plano de entrega:** shadow mode → enforcing no free → enforcing geral.

Decisões que vale você revisar:

- **Deixei de fora o falso positivo com NAT compartilhado** de propósito — você mesmo disse que esse não existe porque o limite é por token e não por IP. Pôr isso como risco seria documentar um problema que não se aplica. Se quiser registrá-lo só como "considerado e não se aplica", eu adiciono.
- **Numeração:** segui a sequência e usei **DD-2026-008** (o anterior é o 007). Se vocês têm outros docs fora dessa pasta ou outra convenção de numeração, me avisa.
- **Estado / Autores / Revisores:** marquei o estado como **Proposto** e deixei autores e revisores em branco (`—`), porque não tenho esses nomes. Me passa quem assina e quem revisa que eu preencho.
- **Tema do objetivo:** o padrão do doc 007 não tem uma seção "Objetivos" separada, mas como você deu objetivos bem explícitos e mensuráveis, abri uma seção curta pra eles. Se preferir manter idêntico ao 007, eu dobro isso dentro do Resumo/Proposta.
