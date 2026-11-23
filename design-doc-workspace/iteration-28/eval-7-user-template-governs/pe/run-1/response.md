Ainda não criei o arquivo. O template tem seções para as quais você não me deu conteúdo, e eu não quero inventá-lo: um plano de rollout fabricado num doc que a arquitetura vai revisar é pior que um buraco.

**O que já tenho (Motivação, Proposta, parte de Métricas):** 4% de duplicatas no mês passado, o impacto no faturamento e as duas reclamações do financeiro. A proposta é um serviço entre o ingestor e o Kafka, com a chave idempotente no Redis por 24h. Descartei as duas alternativas (deduplicar no consumidor e a idempotência nativa do produtor Kafka) com os motivos que você deu. O trade-off aceito é +5ms no caminho crítico, e a meta é ficar abaixo de 0,1% de duplicatas.

**O que falta para seguir o template à risca:**

1. **Plano de rollout.** Como isso entra em produção? Tem fases (ex.: modo sombra só contando duplicatas, depois descarte em parte do tráfego, depois tudo)? Qual o critério para avançar de uma fase para a próxima e qual o gatilho de rollback?
2. **Riscos.** Só tenho o +5ms de latência. Que outros riscos vocês já levantaram, e qual a mitigação de cada um? Se ainda não discutiram, me diga e eu registro isso como pergunta aberta, sem listar riscos por conta própria.
3. **Proposta, nível de componentes e fluxo.**
   - Como é a chave idempotente: vem do produtor ou o serviço a deriva? De que campos ela é composta?
   - O serviço é stateless, com várias instâncias na frente do mesmo Redis?
   - Como ele registra a chave e decide descartar? Por exemplo, uma operação atômica "grava se não existir".

   Com isso eu monto o diagrama e o texto do fluxo. Não vou colocar tecnologia nem protocolo nas caixas e setas além do que você disser.
4. **Métricas de sucesso.** Além de <0,1% de duplicatas, existe um alvo para a latência (ex.: p99 de ingestão não passa de X ms)? E como vocês vão medir a taxa de duplicatas: pela mesma consulta do mês passado?
5. **Perguntas abertas.** O que vocês ainda não sabem? Se não houver nada, eu registro isso.

**Detalhes que vou assumir, se não disser o contrário:**
- **ID do documento:** `DD-2026-001`, porque `docs/design/` só tem o template. Se o time numera de outra forma, me avise.
- **Estado e datas:** estado `Rascunho`, criado e atualizado em 2026-11-23.
- **Revisores:** campo vazio, a menos que você me diga quem são.
- **Arquivo:** `docs/design/dedup-eventos.md`.
- **Alternativas e "fazer nada":** o template não tem seção para isso. Pelo seu relato, as alternativas fazem parte da decisão. Sugiro uma seção extra "Alternativas consideradas" dentro de Proposta, sem mexer na ordem nem nos títulos do template. Posso fazer assim? Se a arquitetura não aceitar nada fora do formato, eu as incluo como parágrafo dentro de Proposta.
