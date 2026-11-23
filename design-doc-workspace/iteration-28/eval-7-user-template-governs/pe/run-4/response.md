Li o template (`docs/design/TEMPLATE.md`). Ele tem seis seções e eu vou seguir todas, na ordem. O que você me passou cobre Motivação e Métricas e boa parte de Proposta. Faltam substância de Riscos e de Plano de rollout, e não vou inventar isso nem preencher com texto genérico. Antes de criar o arquivo, preciso destas respostas:

1. **Riscos:** além dos +5ms no caminho crítico, o que o time acha que pode dar errado? Por exemplo, o que acontece com a ingestão se o Redis ficar indisponível? Descartar um evento legítimo por engano é um risco que vocês consideraram? Para cada risco, qual é a mitigação?
2. **Plano de rollout:** quais são as fases (por exemplo, sombra, percentual de tráfego, 100%)? Qual critério faz avançar de uma fase para a próxima? Qual condição dispara o rollback, e como se faz?
3. **Proposta, detalhes do fluxo:**
   - De onde vem a chave idempotente? O produtor gera, ou o ingestor deriva dos campos do evento?
   - Quando o serviço vê um repetido, ele só descarta ou responde algo ao produtor/ingestor?
   - O serviço roda com quantas instâncias e em que tecnologia? Se isso ainda não foi decidido, eu registro como pergunta aberta.
4. **Cabeçalho:** quem são os revisores? A pasta só tem o template, então vou numerar como `DD-2026-001`. Confirma?

Duas observações sobre o formato:
- O template não tem seção para as **alternativas** que vocês descartaram (dedup no consumidor e idempotência nativa do Kafka). Vou acrescentar uma seção "Alternativas consideradas" dentro de Proposta, sem mexer no esqueleto nem na ordem. Se o time de arquitetura não aceitar subseção extra, me avise.
- Os 4% de duplicatas, a meta de 0,1% e os +5ms entram como você disse. Se o +5ms tiver método de estimativa, me conte para eu registrar.

Com essas respostas eu escrevo e salvo o arquivo.
