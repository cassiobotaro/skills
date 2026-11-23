Li o template e já tenho a base do doc: motivação (4% de duplicatas, faturamento, duas reclamações do financeiro), proposta (serviço entre o ingestor e o Kafka, chave idempotente no Redis por 24h), as duas alternativas descartadas, o trade-off de +5ms e a meta de menos de 0,1%.

Ainda não criei o arquivo. O template exige as seções Riscos, Plano de rollout e Perguntas abertas, e você não me deu o conteúdo delas. Não vou inventar esse conteúdo nem deixar as seções vazias. Antes de escrever, preciso de respostas para estas perguntas:

1. **Riscos.** Que riscos o time enxerga nessa proposta e como pretende mitigar cada um? Além do +5ms, que você já aceitou, vocês discutiram algum outro risco? Pode ser "nenhum discutido ainda", e eu registro isso como pergunta aberta.
2. **Plano de rollout.** Como o serviço entra em produção? Preciso das fases (por exemplo, shadow mode, depois uma parte dos produtores, depois todos), do critério para avançar de fase e do critério e mecanismo de rollback.
3. **Métricas de sucesso.** A meta é duplicatas abaixo de 0,1%. Como vocês vão medir isso: com a mesma metodologia que deu os 4%, sobre qual janela? Existe alguma meta para a latência, por exemplo p99 com teto em +5ms, ou os 5ms são só uma estimativa?
4. **Perguntas abertas.** O que ainda está indefinido? Se não houver nada, eu registro isso explicitamente.
5. **Cabeçalho.**
   - Quem são os revisores, ou deixo em branco?
   - O número do documento será DD-2026-001? A pasta não tem outros docs, então não tenho uma sequência para continuar.
   - O estado fica como "Rascunho"?

Os dois itens a seguir não são do template. Quero seu aval antes de incluí-los:

- **Alternativas consideradas.** O template não tem seção para elas, e as duas que você descreveu (deduplicar no consumidor e idempotência nativa do produtor Kafka) são parte central do raciocínio. Proponho uma seção "Alternativas consideradas" dentro de Proposta, ou logo depois dela, mantendo a ordem e os títulos do template. Pode ser? Se vocês também consideraram "não fazer nada", me diga o motivo.
- **Como chega a chave idempotente.** Quem gera a chave e onde ela viaja no evento? O que o serviço faz quando o Redis não responde? Isso pode ser uma pergunta aberta ou parte da Proposta, como você preferir. Não vou assumir uma resposta.

Com essas respostas eu escrevo e salvo em `docs/design/`.
