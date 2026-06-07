# DD-2026-008 · Rate limiting da API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Em revisão |
| **Autores** | Cássio Botaro |
| **Revisores** | _a definir_ |
| **Criado em** | 2026-06-07 |
| **Última atualização** | 2026-06-07 |
| **Tags** | api, rate-limiting, kong, redis, confiabilidade |

## Resumo

Hoje a API pública não tem nenhum limite por cliente: no incidente INC-4412 um cliente com integração mal feita enviou 40x o tráfego normal e derrubou a API para todos por 25 minutos. Este documento propõe rate limit por token de API no gateway (Kong), com janela deslizante apoiada nos contadores do Redis que já usamos para sessão, limites por plano e resposta 429 com `Retry-After`. O objetivo é que nenhum token exceda seu limite por mais de 1s e que um cliente abusivo não degrade os demais.

## Contexto

A API pública não impõe nenhum limite de taxa por cliente. Qualquer token pode enviar tráfego ilimitado, e a capacidade da API é compartilhada entre todos sem isolamento.

No incidente INC-4412 um cliente com integração mal feita passou a enviar cerca de 40x o tráfego normal. Sem nenhum limite que o contivesse, ele saturou a API e a deixou indisponível para todos os clientes por 25 minutos.

Os clientes da API pública estão divididos em três planos comerciais — free, pro e enterprise —, mas essa divisão hoje não tem nenhum reflexo técnico no tráfego que cada um pode gerar. O Redis usado para sessão já está em produção no caminho da API.

## Proposta

Aplicar rate limit **por token de API** no gateway Kong, usando **janela deslizante** com contadores no **Redis** que já usamos para sessão. O limite é por plano:

- **free:** 10 rps
- **pro:** 100 rps
- **enterprise:** negociado por contrato

Quando um token excede o limite da janela, o gateway responde **429 Too Many Requests** com o header **`Retry-After`** indicando ao cliente quando voltar a tentar. A decisão acontece no gateway, antes de a requisição consumir qualquer serviço ou a malha interna.

A escolha por limitar **por token** (e não por IP) é deliberada: o limite acompanha o cliente comercial, não a origem de rede. Chegamos a anotar o risco de falso positivo com NAT compartilhado, mas ele não se aplica aqui — como o limite é por token, dois clientes atrás do mesmo NAT têm contadores independentes.

### Compensações

- ✓ Um cliente abusivo é contido no gateway, sem chegar aos serviços nem à malha, preservando a API para os demais — o que faltou no INC-4412.
- ✓ Os limites por plano dão um significado técnico à divisão comercial e tornam o comportamento previsível por cliente.
- ✓ Reaproveita o Redis de sessão já em produção, sem nova peça de infraestrutura nem custo adicional de licença.
- ✗ Um cliente legítimo em pico (ex.: Black Friday) pode tomar 429 ao ultrapassar o limite do seu plano. Mitigamos com o `Retry-After` para que o cliente recue de forma ordenada e com um alerta para o time de contas avisar os clientes enterprise antecipadamente.
- ✗ O Redis de sessão passa a estar também no caminho de cada decisão de rate limit, o que aumenta seu acoplamento e sua importância (ver Riscos).

### Alternativas consideradas

- **Não fazer nada.** Mantém a API exposta a uma repetição do INC-4412: qualquer token mal comportado pode derrubar todos. Descartado.
- **Limitar dentro de cada serviço.** Descartado: é tarde demais. Quando a requisição chega ao serviço, ela já consumiu o gateway e a malha interna — exatamente os recursos que saturaram no incidente. O ponto certo de corte é a entrada, no gateway.
- **Módulo pago de rate limiting do gateway gerenciado.** Descartado por custo e por lock-in no fornecedor. A janela deslizante sobre o Redis que já operamos entrega o mesmo controle sem essa dependência.

### Critério de sucesso

- Nenhum token excede seu limite de plano por mais de 1s.
- A API absorve um cliente abusivo (padrão INC-4412) sem degradar a latência ou a disponibilidade dos demais clientes.

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão virar ponto de contenção ao assumir também os contadores de rate limit | Medir o impacto antes de ativar o enforcing (ver Plano de entrega — o shadow mode existe justamente para essa medição) |

## Plano de entrega

1. **Shadow mode** — o gateway apenas mede o que limitaria, sem responder 429. Serve para validar os limites por plano e medir o impacto dos contadores sobre o Redis de sessão antes de qualquer corte de tráfego.
2. **Enforcing no plano free** — ativa o 429 + `Retry-After` apenas para os tokens do plano free, o grupo de menor risco comercial.
3. **Enforcing geral** — estende o enforcing a pro e enterprise.
