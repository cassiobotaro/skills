O documento está pronto e o autoreview passou (nada inventado, seções do padrão da casa cobertas na ordem, data real, voz ativa). Segue minha resposta final ao usuário, em português:

---

Dei uma olhada em `docs/design/` e segui o padrão do DD-2026-007: tabela de cabeçalho, Resumo, Contexto, Proposta com Compensações (✓/✗), Riscos em tabela e Plano de entrega. Criei o doc novo em:

**`docs/design/dd-2026-008-rate-limiting-api-publica.md`**

O que ele registra:

- **Contexto**: o INC-4412 (cliente com 40× o tráfego normal, API fora do ar por 25 min) e a ausência de qualquer limite por cliente hoje.
- **Objetivos**: os dois que vocês fecharam — nenhum token excede seu limite por mais de 1s, e a API sustenta um cliente abusivo sem degradar os demais.
- **Proposta**: rate limit por token no Kong, janela deslizante com contadores no Redis de sessão, limites por plano (free 10 rps, pro 100 rps, enterprise negociado), `429` com `Retry-After`. Aproveitei sua observação sobre o NAT e registrei como característica do design (limite por token, não por IP, então NAT compartilhado não gera falso positivo) — não como risco, já que vocês concluíram que ele não existe.
- **Compensações**: o custo aceito está explícito — cliente legítimo em pico (Black Friday) pode tomar `429`, mitigado pelo `Retry-After` e pelo alerta ao time de contas; e o Redis de sessão entra no caminho crítico de toda requisição.
- **Alternativas**: limitar dentro de cada serviço (tarde demais) e o módulo pago do gateway gerenciado (custo e lock-in). Acrescentei "não fazer nada", descartada porque sem limite o INC-4412 se repete — é convenção nossa registrar essa alternativa; se preferir tirar, é só remover o item 3.
- **Riscos**: o Redis virar ponto de contenção, com a mitigação que vocês definiram (medir na fase de shadow mode, antes do enforcing).
- **Plano de entrega**: shadow mode → enforcing no free → enforcing geral.

Duas seções fugiram do DD-2026-007 (**Objetivos** e **Alternativas consideradas**): adicionei porque você trouxe esse conteúdo pronto e ele é o que dá valor de longo prazo ao doc — me avisa se o padrão da casa preferir esse material dentro do Contexto e da Proposta.

Ficaram três lacunas que só você pode preencher — deixei o cabeçalho marcado com *(a preencher)*:

1. **Autores**: quem assina o doc (você e mais alguém do war room?).
2. **Revisores**: quem revisa, com a área — sugiro alguém de Plataforma/gateway (dono do Kong), alguém de SRE (dono do Redis) e, pelo impacto nos clientes enterprise, alguém do time de contas.
3. **Critério de saída do shadow mode**: qual medida no Redis (ou nos contadores) libera a fase de enforcing? Hoje o doc diz só "medir antes" — se vocês tiverem um limiar em mente, vale registrar na tabela de Riscos.
