Doc escrito. Minha resposta final ao usuário, em português:

---

Criei o doc seguindo o padrão de `docs/design/` (usei o DD-2026-007 como referência de estrutura: cabeçalho em tabela, Resumo, Contexto, Proposta com Compensações, Riscos, Plano de entrega, e continuei a numeração):

**`docs/design/dd-2026-008-rate-limiting-api-publica.md`**

O que está lá:

- **Resumo e Contexto** ancorados no INC-4412: 40x o tráfego normal, 25 minutos de indisponibilidade para todos, nenhum limite por cliente hoje.
- **Proposta** com os dois objetivos mensuráveis (nenhum token excede o limite por mais de 1s; cliente abusivo não degrada os demais), limite por token no Kong, janela deslizante no Redis de sessão, tabela de limites por plano (free 10 rps, pro 100 rps, enterprise negociado) e `429` + `Retry-After`. Incluí um diagrama de sequência Mermaid do fluxo no gateway, com o texto explicando os passos. *Observação: não havia validador Mermaid disponível aqui (nem MCP nem mermaid-cli), então o diagrama não foi validado por máquina — usei só sintaxe portável; GitHub/GitLab renderam direto, e dá pra conferir em mermaid.live.*
- **Compensações** com o custo aceito explícito: cliente legítimo em pico (Black Friday) pode tomar `429`, mitigado com `Retry-After` + alerta pro time de contas avisar os enterprise.
- **Alternativas consideradas** — essa seção não existe no DD-2026-007, mas o war room descartou duas alternativas reais (limitar dentro de cada serviço; módulo pago do gateway gerenciado) e esse raciocínio é o valor de longo prazo do doc, então adicionei, incluindo o "não fazer nada". Se o padrão da casa não permite seções extras, é só me avisar que eu realoco.
- **Riscos**: só o que vocês levantaram — o Redis de sessão como ponto de contenção, com a medição no shadow mode como mitigação. O falso positivo de NAT ficou **de fora**, como você mesmo concluiu (limite por token, não por IP) — registrei essa razão brevemente na Proposta, porque é uma pergunta que um revisor vai fazer.
- **Plano de entrega** nas três fases: shadow mode → enforcement no free → enforcement geral. Não inventei prazos.

Três coisas que só você pode responder (o doc está em Rascunho até lá):

1. **Autores e revisores** — deixei como *(a preencher)* no cabeçalho. Sugeri Plataforma, SRE e time de contas como áreas revisoras, pelas partes que o design toca (Kong, Redis, comunicação com enterprise); quem são as pessoas?
2. **Comportamento com Redis indisponível** — se o Redis cair ou ficar lento, o Kong deixa passar sem limite (fail-open) ou rejeita (fail-closed)? Isso decide o comportamento da API justamente no cenário de contenção que vocês querem medir, e hoje não está no doc.
3. **Critério para avançar de fase** — o que encerra o shadow mode (tempo? um número de carga no Redis considerado aceitável?)? Se houver um critério combinado, vale registrar no plano de entrega.
