Olhei o que já existe em `docs/design/` (só o `dd-2026-007-cache-de-catalogo.md`) e segui o padrão da casa: título `DD-AAAA-NNN · ...`, tabela de metadados, e as seções **Resumo → Contexto → Proposta (com Compensações) → Riscos → Plano de entrega**. Escrevi o doc novo aqui:

`docs/design/dd-2026-008-rate-limiting-api-publica.md`

O que coloquei, tudo a partir do que você passou e do war room:

- **Contexto:** só o pano de fundo — INC-4412, 40x o tráfego, 25 min de queda, ausência de limite por cliente hoje. Deixei objetivo e solução fora daqui (eles vão pra Resumo/Proposta).
- **Proposta:** rate limit por token no Kong, janela deslizante sobre o Redis de sessão, limites por plano (free 10 rps, pro 100 rps, enterprise negociado), 429 + `Retry-After`, decisão no gateway antes de consumir serviço e malha.
- **Compensações:** os ganhos e, explícito, o custo aceito (cliente legítimo em pico tipo Black Friday pode tomar 429, mitigado com `Retry-After` + alerta pro time de contas). Adicionei também que o Redis de sessão passa a ter mais peso no caminho crítico.
- **Alternativas consideradas:** limitar dentro do serviço (tarde demais), módulo pago do gateway gerenciado (custo + lock-in) e "não fazer nada". Como o doc de referência não tem seção própria de alternativas, encaixei como subseção dentro da Proposta (do mesmo jeito que Compensações), pra não descartar essa parte do raciocínio nem quebrar a estrutura da casa.
- **Critério de sucesso:** seu objetivo, medível — nenhum token excede o limite por mais de 1s e a API aguenta um cliente abusivo sem degradar os demais. Também ficou como subseção da Proposta, pelo mesmo motivo.
- **Riscos:** só o Redis de sessão virar ponto de contenção, com a mitigação de medir antes (o shadow mode serve pra isso). **Não** registrei o falso positivo de NAT compartilhado como risco — você foi claro que ele não existe porque o limite é por token; mencionei na Proposta que foi considerado e por que não se aplica, mas não como risco real.
- **Plano de entrega:** shadow mode (medindo, inclusive o impacto no Redis) → enforcing no free → enforcing geral.

Duas coisas que preenchi por padrão e que você pode querer ajustar:

1. **Autores/Revisores:** botei você como autor e deixei **Revisores: a definir**. Quem participou do war room deveria entrar como revisor? Me passa os nomes e as áreas (ex.: Plataforma, SRE) que eu ajusto.
2. **Estado:** deixei **Em revisão**. Se a decisão já está fechada e o doc é pra registro, posso mudar pra Aprovado.

Uma pergunta de substância, se quiser fechar o doc: existe algum número de capacidade da API (rps em pico, ou o que o INC-4412 atingiu) que valha citar no Contexto? O doc de cache cita rps e P99; se você tiver os equivalentes aqui, deixo o Contexto mais concreto.
