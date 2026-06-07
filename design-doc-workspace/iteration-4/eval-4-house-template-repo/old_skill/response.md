Escrevi o doc seguindo o padrão de `docs/design/` (mesma tabela de metadados, seções e estilo do DD-2026-007), no próximo ID da sequência:

**`docs/design/dd-2026-008-rate-limiting-api-publica.md`** — *DD-2026-008 · Rate limiting da API pública* (Estado: Aprovado, criado em 2026-06-07).

Estrutura:

- **Resumo / Contexto** — o INC-4412 (cliente com integração mal feita, 40x o tráfego, API derrubada por 25 min) e o fato de hoje não haver limite por cliente.
- **Objetivos** — os dois mensuráveis que você fechou: nenhum token excede o limite por mais de 1s, e a API aguenta um cliente abusivo sem degradar os demais.
- **Proposta** — rate limit por token no Kong, janela deslizante com contadores no Redis de sessão, limites por plano (free 10 rps, pro 100 rps, enterprise negociado) e `429` + `Retry-After`.
- **Compensações** — incluindo o trade-off aceito: cliente legítimo em pico (Black Friday) pode tomar `429`, mitigado pelo `Retry-After` e pelo aviso do time de contas aos enterprise.
- **Alternativas consideradas** — limitar dentro do serviço (tarde demais, já consumiu gateway/malha), o módulo pago do gateway gerenciado (custo e lock-in), e "não fazer nada" (mantém a exposição do INC-4412).
- **Riscos** — o Redis de sessão virar ponto de contenção, com a mitigação de medir antes de ativar o enforcing.
- **Plano de entrega** — shadow mode → enforcing no free → enforcing geral.

Duas decisões que vale registrar:

1. Deixei de fora o falso positivo de NAT/IP compartilhado — você mesmo notou que não se aplica aqui, já que o limite é por token e não por IP. Não inventei risco que não existe.
2. Acrescentei seções de **Objetivos** e **Alternativas** que o DD-2026-007 não tinha; como você forneceu objetivos mensuráveis e alternativas reais, elas registram o raciocínio sem fugir do estilo da casa. Se preferir manter o doc mais enxuto (só Resumo/Contexto/Proposta/Riscos/Plano, como o 007), é só avisar que eu colapso.

Os campos **Autores** e **Revisores** ficaram como `—` — me passe os nomes (e as áreas dos revisores, como no 007: "João Prata (Plataforma)") que eu preencho.
