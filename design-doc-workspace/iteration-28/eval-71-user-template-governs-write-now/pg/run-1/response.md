Escrevi o documento em `docs/design/dd-2026-001-deduplicacao-de-eventos.md`, seguindo o `TEMPLATE.md` na ordem dele. Ainda não commitei.

**O que ficou preenchido, só com o que você disse**
- **Motivação:** 4% de duplicatas no mês passado, reenvio em retry e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, a chave no Redis por 24h e o descarte de repetidos.
- **Alternativas e trade-off:** as duas alternativas descartadas, com o motivo de cada uma, e o custo aceito de +5 ms.
- **Métricas de sucesso:** duplicatas abaixo de 0,1%, contra a linha de base de 4%.

**Onde fugi do template**
- Acrescentei uma subseção "Alternativas consideradas" dentro de Proposta, porque o template não tem lugar para elas. Também pus "Trade-off aceito" nessa seção. A ordem das seções do template não mudou.
- Os campos **Revisores** e **Plano de rollout** ficaram sem conteúdo. Você não falou de rollout, então a seção só aponta para as perguntas.
- A seção **Riscos** traz só o +5 ms. Não inventei outros riscos.
- **DD-2026-001:** assumi esse número porque a pasta não tem outros documentos. Deixei isso como pergunta, caso a arquitetura use outra numeração.

**Perguntas abertas (15)**
As mais importantes são estas:
- O que acontece se o Redis cair ou ficar lento?
- De onde vem a chave idempotente?
- A gravação da chave e o envio ao Kafka são atômicos?
- Como é o rollout?
- Por que 24h?
- Alguém considerou não fazer nada?
- Os +5 ms foram medidos ou estimados?

Quando você responder, é só me passar as respostas que eu atualizo as seções de Riscos, Rollout e Proposta.
