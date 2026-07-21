Escrevi o doc em `docs/design/dd-2026-008-rate-limiting-da-api-publica.md`, seguindo o padrão do DD-2026-007: mesma tabela de cabeçalho, mesmas seções (Resumo → Contexto → Proposta → Compensações → Riscos → Plano de entrega), mesma convenção de nome de arquivo e continuando a numeração.

**O que ficou no doc**

- **Resumo/Contexto**: o INC-4412 (40x o tráfego normal, 25 minutos de API fora para todos) e a ausência de qualquer limite por cliente hoje.
- **Proposta**: rate limit por token no Kong, janela deslizante com contadores no Redis de sessão, limites por plano (free 10 rps, pro 100 rps, enterprise negociado), 429 com Retry-After. Incluí um diagrama de sequência Mermaid do caminho da requisição (validado e renderizado) seguido da explicação em prosa.
- **Compensações**: os ganhos (corte no gateway antes de consumir malha e serviços, reaproveitamento de Kong e Redis) e os custos aceitos (cliente legítimo em pico pode tomar 429; o Redis de sessão entra no caminho crítico de toda requisição).
- **Riscos**: contenção no Redis de sessão (medir no shadow mode) e o 429 no cliente legítimo (Retry-After + alerta pro time de contas).
- **Plano de entrega**: shadow mode → enforcing free → enforcing geral.

**Duas coisas que fiz diferente do DD-2026-007** — o repositório só tem um doc, então inferi o padrão dele e precisei estender:

1. Criei **## Objetivos** para o alvo que você deu (nenhum token excede o limite por mais de 1s; a API aguenta um abusivo sem degradar os demais). Não achei lugar honesto pra isso nas seções existentes — objetivo não é contexto.
2. Criei **## Alternativas consideradas**, com o limite dentro de cada serviço, o módulo pago do gateway gerenciado e o "não fazer nada" (refutado pelo próprio INC-4412). É a seção que dá valor de longo prazo ao doc, e o DD-2026-007 provavelmente não a tem só porque não houve alternativa real lá.

**Deixei de fora de propósito**: o falso positivo com NAT compartilhado, já que o limite é por token e não por IP — o cenário não existe. Registrei no texto a frase equivalente e verdadeira ("o escopo do limite é o token, não o endereço de origem"), pra ninguém levantar isso de novo na revisão.

**O que preciso de você pra fechar o cabeçalho e o doc:**

1. **Autores e revisores** — quem assina, e quais áreas devem revisar? Sugiro alguém de Plataforma/gateway e de SRE (o Redis de sessão passa a ser dependência da API pública inteira), no mesmo formato do DD-2026-007 ("Nome (Área)").
2. **Estado** — deixei como *Rascunho*. Se a proposta já foi fechada no war room, ele já nasce "Em revisão"?
3. **Existe um template oficial do padrão de design doc** (wiki, drive) ou o DD-2026-007 é a referência de fato? Se houver, me passa que eu ajusto as seções que inventei (Objetivos, Alternativas) pros nomes canônicos.
4. **Limite do plano enterprise** — "negociado" fica assim mesmo no doc, ou existe um teto/valor padrão que vale a pena registrar?
5. **Como o time vai observar isso?** O DD-2026-007 não tem seção de observabilidade, mas o objetivo "nenhum token excede o limite por mais de 1s" pede uma métrica que prove isso. Tem dashboard/alerta previsto? Se sim, eu acrescento uma linha no plano de entrega ou uma seção curta.
