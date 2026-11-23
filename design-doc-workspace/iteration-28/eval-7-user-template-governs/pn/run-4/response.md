Li o template e vou seguir as seis seções na ordem (Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso, Perguntas abertas). Ainda não criei o arquivo. Com o que você me passou, Motivação, Proposta e Métricas estão cobertas. Faltam fatos para Riscos e Rollout, e prefiro perguntar a inventar. Não existe nenhum DD anterior em `docs/design/`, então o documento será `DD-2026-001`.

**Riscos**
1. **Redis indisponível.** O serviço fica no caminho crítico, então a decisão importa. Em caso de falha do Redis ele deve deixar o evento passar (*fail-open*, volta a ter duplicatas) ou bloquear a ingestão (*fail-closed*, nenhum evento duplicado, mas há perda de disponibilidade)? Se essa decisão ainda está em aberto, registro como pergunta aberta.
2. **Outros riscos conhecidos.** Por exemplo, o próprio serviço cair, o Redis perder dados num failover ou reenvios que chegam depois de 24h. Algum desses já foi discutido? Quais mais você quer listar, e qual a mitigação de cada um?

**Plano de rollout**
3. Como o serviço entra em produção? Preciso das fases (por exemplo, modo sombra, que só mede, e depois um percentual de produtores ou tráfego), do critério para avançar de uma fase para a seguinte e de como se faz rollback. Se isso ainda não foi definido, posso registrar como pergunta aberta, mas a seção ficará com pouco conteúdo.

**Cabeçalho e detalhes**
4. Quem são os revisores (o time de arquitetura, nomes específicos)?
5. Qual é a chave idempotente do evento? Ela vem do produtor ou o serviço a calcula? Se não estiver decidido, entra em Perguntas abertas.

Os 4% de duplicatas, a meta de menos de 0,1% e os +5ms de latência vão como você os informou. Você não deu um limite de latência aceitável nem a fonte dos 4% além de "mês passado". Se houver um teto (por exemplo, p99), me diga. Se não, a seção só cita a estimativa de +5ms.

Também vou colocar as alternativas descartadas (dedup no consumidor e idempotência nativa do Kafka) dentro de Proposta, como subseção. O template não tem seção própria para elas, e prefiro não alterar o esqueleto.

Me responda o que souber e eu escrevo o arquivo em seguida.
