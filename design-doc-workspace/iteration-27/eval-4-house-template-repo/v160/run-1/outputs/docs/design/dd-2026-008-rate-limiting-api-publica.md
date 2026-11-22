# DD-2026-008 · Rate limiting da API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | A definir (ver Questões em aberto) |
| **Revisores** | A definir (ver Questões em aberto) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |
| **Tags** | api, gateway, rate-limiting, redis, kong |

## Resumo

Hoje a API pública não tem nenhum limite de requisições por cliente. No incidente INC-4412, um único cliente derrubou a API para todos. Este documento propõe limitar as requisições por token de API no gateway (Kong), com janela deslizante e contadores no Redis, limites por plano e resposta 429 com o header `Retry-After`. A entrega acontece em três fases: shadow mode, enforcing no plano free e enforcing geral.

## Contexto

Em 2026-11-21, um cliente com uma integração mal feita enviou 40x o tráfego normal e a API ficou fora do ar para todos os clientes por 25 minutos (INC-4412). Hoje não existe nenhum limite por cliente.

O gateway é o Kong. O Redis que guarda as sessões já está em uso e é a base escolhida para os contadores.

Os limites variam por plano:

| Plano | Limite |
|---|---|
| Free | 10 rps |
| Pro | 100 rps |
| Enterprise | Negociado por cliente |

Aqui, rps significa requisições por segundo.

## Objetivos

- Nenhum token excede o seu limite por mais de 1s.
- A API aguenta um cliente abusivo sem degradar os demais.

## Proposta

O Kong conta as requisições de cada token de API numa janela deslizante, com os contadores no Redis de sessão. Quando um token ultrapassa o limite do seu plano, o Kong responde 429 com o header `Retry-After` e a requisição não segue para os serviços. O limite é por token e não por IP.

### Compensações

- ✓ O Kong rejeita a requisição excedente antes que ela consuma recursos da malha de serviços.
- ✓ Os contadores usam o Redis que a equipe já opera, sem infraestrutura nova.
- ✓ Sem módulo pago, sem custo de licença e sem lock-in com o gateway gerenciado.
- ✗ Um cliente legítimo em pico (Black Friday, por exemplo) pode receber 429. O `Retry-After` indica quando tentar de novo e um alerta avisa o time de contas, que avisa os clientes enterprise.
- ✗ O Redis de sessão passa a receber as escritas dos contadores e pode virar ponto de contenção.

### Alternativas consideradas

| Alternativa | Resultado | Motivo |
|---|---|---|
| Não fazer nada | ✗ Descartada | Continuam sem limite por cliente, e um cliente que envia 40x o tráfego normal derrubou a API por 25 minutos (INC-4412). |
| Limitar dentro de cada serviço | ✗ Descartada | Tarde demais: a requisição já consumiu o gateway e a malha. |
| Módulo pago do gateway gerenciado | ✗ Descartada | Custo e lock-in. |
| Limite por token no Kong, com Redis | ✓ Escolhida | Rejeita na entrada, reaproveita o Redis existente e não tem custo de licença. |

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão vira ponto de contenção | Medir a carga dos contadores antes de ativar o enforcing (a fase em shadow mode serve a isso) |
| Cliente legítimo em pico recebe 429 | Header `Retry-After` na resposta e alerta para o time de contas avisar os clientes enterprise |

## Plano de entrega

1. Shadow mode: o Kong conta e registra quem excederia o limite, sem rejeitar nenhuma requisição.
2. Enforcing no plano free.
3. Enforcing em todos os planos.

## Questões em aberto

- Quem são os autores e quais áreas devem revisar (Plataforma, SRE, time de contas)?
- Qual o prazo de cada fase e qual o critério para passar de uma para a outra?
- O que o Kong faz com a requisição quando o Redis está indisponível: deixa passar ou rejeita?
- O que fica fora do escopo desta entrega?
- Como e com que métrica a equipe vai medir a carga no Redis de sessão antes do enforcing?
