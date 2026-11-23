Salvei o documento em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Não rodei `scripts/validate.py` nem `claude plugin validate`. A única checagem foi reler o template.

O documento segue as seis seções do template, na mesma ordem e com o cabeçalho em tabela. Só `TEMPLATE.md` existia na pasta, então usei o ID `DD-2026-001` e o estado Rascunho. Você aparece como autor e a data é 2026-11-23.

**O que está no documento**
- **Motivação:** os 4% de duplicatas do mês passado e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave no Redis por 24h. Também registra o trade-off aceito, de +5 ms no caminho crítico.
- **Riscos:** só a latência está preenchida, porque foi o único risco que você citou. Marquei como estimativa o valor de 5 ms.
- **Plano de rollout:** ficou como "ainda não definido", com remissão às perguntas.
- **Métricas de sucesso:** duplicatas abaixo de 0,1% e a latência real medida contra os 5 ms estimados.
- **Perguntas abertas:** 10 perguntas, agrupadas por seção. Cobrem o comportamento quando o Redis cai, a composição da chave idempotente, a ordem entre gravar a chave e publicar no Kafka, as fases e o critério de rollback, os revisores e como se mede a taxa de duplicatas.

**Desvios do template**
- Acrescentei a subseção "Alternativas consideradas" dentro de Proposta. O template não tem lugar para elas, e o motivo do descarte das duas opções que vocês discutiram não devia se perder. A ordem das seções do template não mudou. Se a arquitetura não aceitar isso, é só mover o conteúdo.
- Não fiz diagrama. Ele pediria detalhes que você não deu, como protocolos e a ordem entre gravar a chave e publicar no Kafka. Isso virou a pergunta 7.

O campo Revisores está vazio de propósito.
