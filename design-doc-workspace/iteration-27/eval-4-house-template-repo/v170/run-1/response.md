Escrevi o doc em `docs/design/dd-2026-008-rate-limiting-api-publica.md`, com estado **Rascunho**. Não commitei nada.

O único doc que já existia era o `dd-2026-007-cache-de-catalogo.md`, e segui a estrutura dele. O cabeçalho é a tabela de metadados, e as seções são Resumo, Contexto, Proposta com Compensações (✓/✗), Riscos e Plano de entrega. O ID continua a sequência (008).

Seu briefing tinha duas coisas que o padrão não comporta. Elas ganharam seção própria, sem mexer na ordem do resto:
- **Objetivos:** os dois objetivos e a tabela de limites por plano ficam depois de Contexto.
- **Alternativas consideradas:** vem depois de Compensações e traz as duas alternativas descartadas. Incluí também "não fazer nada", com o INC-4412 como motivo.

Fiz mais duas coisas fora do que você pediu:
- **Questões em aberto:** acrescentei essa seção no fim, para registrar o que o briefing não cobria.
- **NAT:** tirei a nota de falso positivo. Só deixei uma frase em Proposta dizendo que o limite vale por token, não por IP.

**Preciso de você:**
- **Autor:** pus `cassiobotaro`, que é o git user. Troque se não for você.
- **Revisores:** deixei "A definir". Vale incluir Plataforma, SRE e o time de contas.

**Questões em aberto no doc:**
- **Redis fora do ar:** não sei o que acontece com as requisições quando ele fica indisponível. Fica aberto porque você não definiu, e é uma decisão de design.
- **Limite enterprise:** quem configura o limite negociado de cada cliente, e onde esse valor fica registrado.
- **Gatilho do alerta:** qual condição dispara o alerta para o time de contas.
- **Fases do plano de entrega:** os critérios para passar de uma fase à seguinte, e quanto tempo dura cada uma. Não inventei prazos.

**Sobre o NAT:** concordo que o limite por token resolve o NAT. Fica a pergunta contrária, que não pus no doc: um cliente consegue emitir vários tokens e dividir o tráfego entre eles? Se sim, o limite por token tem uma brecha.

Rodei o `technical-writing` (reescrevi duas frases com sujeito oculto) e o `unslop` (sem ajustes). Não sobrou travessão nem passiva sem agente.
