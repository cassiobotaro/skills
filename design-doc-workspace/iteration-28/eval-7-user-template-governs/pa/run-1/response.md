Ainda não criei o arquivo. O template exige Riscos, Plano de rollout e Perguntas abertas, e você não me deu o conteúdo dessas seções. Prefiro perguntar a inventar. O resto já tenho: motivação com os 4% e as reclamações do financeiro, a proposta, as duas alternativas descartadas, o trade-off dos +5ms e a meta de 0,1%.

**Plano de rollout** (nada informado)
1. Como o serviço entra em produção? Por exemplo: modo sombra (só mede duplicatas sem descartar), depois uma fração do tráfego, depois 100%. Ou outro caminho?
2. Qual o critério para avançar de uma fase para a outra e qual o gatilho de rollback?

**Riscos** (só o +5ms de latência foi informado)
3. O que acontece se o Redis cair ou ficar lento? O serviço deixa passar o evento (fail-open, podem voltar duplicatas) ou bloqueia a ingestão (fail-closed)? Qual foi a decisão do time?
4. Há outros riscos que vocês já discutiram? Por exemplo: o próprio serviço como ponto único de falha, perda de dados do Redis, falso positivo descartando evento legítimo, ou a duplicata que chega depois de 24h.

**Detalhes da proposta**
5. Qual é a chave idempotente? Os produtores já mandam um ID de evento ou isso muda o contrato com eles?
6. Existe algo fora do escopo, ou algum constraint que eu deva registrar?

**Cabeçalho e perguntas abertas**
7. Quem são os revisores?
8. O que ainda não se sabe? Se não houver nada, escrevo isso explicitamente em vez de inventar.

**Número do documento.** A pasta só tem o `TEMPLATE.md`, então não há sequência anterior. Vou usar `DD-2026-001`, a não ser que vocês numerem de outra forma.

**Alternativas.** O template não tem seção para elas. Vou criar uma seção "Alternativas consideradas" logo depois de Proposta, com "não fazer nada" (manter os 4%) e as duas que você citou. O resto do template fica intacto, na mesma ordem. Se a arquitetura não aceitar esse acréscimo, me avise e eu dobro as alternativas dentro da Proposta.

Para eu seguir, basta responder o que souber. O que você deixar em branco vira pergunta aberta no documento.
