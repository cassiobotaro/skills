Ainda não criei o arquivo. Pelo template, todas as seções precisam estar preenchidas, e Riscos e Plano de rollout não têm conteúdo na sua descrição. Não quero inventar nem deixar essas seções com texto genérico. Cinco perguntas:

1. **Rollout:** como o serviço entra em produção? Por exemplo, modo sombra (só marca duplicatas, sem descartar), depois uma fração dos produtores, depois todos. Qual critério faz cada fase avançar, e qual dispara o rollback?
2. **Risco do Redis:** se o Redis ficar indisponível ou lento, o serviço deixa passar tudo (*fail-open*, volta a ter duplicatas) ou bloqueia a ingestão (*fail-closed*)? Quais outros riscos vocês veem e como mitigam cada um? Alguns candidatos: perda de dados do Redis, descartar um evento legítimo e o salto extra como ponto único de falha.
3. **Chave idempotente:** quem gera a chave? Os produtores já mandam uma hoje, ou isso é uma mudança que eles também terão de fazer? Se ainda não está decidido, registro em Perguntas abertas.
4. **Métricas:** além de duplicatas abaixo de 0,1%, existe um teto de latência para o +5ms, por exemplo p99? E como vocês mediram os 4% do mês passado? Quero usar a mesma medição como linha de base.
5. **Cabeçalho:** a pasta só tem o TEMPLATE, então proponho `DD-2026-001`. Está certo? Quem são os revisores? Se ainda não definiu, deixo em branco.

Duas decisões minhas, para você corrigir se quiser:
- As alternativas descartadas (deduplicar no consumidor e idempotência nativa do produtor Kafka) e a meta de 0,1% não têm seção própria no template. Vou colocá-las dentro de **Proposta**, em subseções, sem mudar a estrutura nem a ordem do template.
- Vou deixar **Criado em** e **Última atualização** com a data de hoje, 2026-11-23, e o **Estado** como Rascunho.
