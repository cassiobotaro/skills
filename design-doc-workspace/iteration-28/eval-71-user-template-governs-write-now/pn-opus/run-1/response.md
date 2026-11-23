Escrevi o documento em `docs/design/DD-2026-001-servico-de-deduplicacao-de-eventos.md`, com as seções do TEMPLATE.md na mesma ordem. Ele está como Rascunho, com data de 2026-11-23.

**Uma mudança em relação ao template:** acrescentei uma seção **Alternativas consideradas** logo depois de Proposta. O template não tem lugar para as alternativas descartadas, e são elas que explicam a forma da proposta. Coloquei também "não fazer nada" como alternativa, usando a dor que você descreveu. Isso está avisado no próprio texto da seção. Se o time de arquitetura não aceitar, dá para passar esse conteúdo para dentro de Proposta. O custo aceito (+5 ms, mais um salto no caminho crítico) ficou numa subseção de Proposta.

**O que ficou incompleto:** Riscos, Plano de rollout e parte de Métricas de sucesso não têm conteúdo próprio, porque você não falou sobre eles. Em vez de inventar, essas seções dizem o que já se sabe e apontam para as perguntas numeradas. A sequência mostra só o que você descreveu e não diz quais protocolos ligam os componentes.

**Ficaram 13 perguntas no final.** As mais importantes:
- Como o serviço se comporta se o Redis cair: deixa passar os eventos sem deduplicar ou trava a ingestão?
- Quem gera a chave idempotente, e se todos os produtores já mandam essa chave.
- Se consultar e gravar a chave no Redis é uma operação atômica, e se a chave é gravada antes ou depois de o Kafka confirmar a publicação.
- Se algum produtor reenvia depois de 24h, que é a janela em que o serviço reconhece um reenvio.
- Fases do rollout, critério de rollback e a latência máxima aceitável (e em qual percentil).

O campo Revisores ficou vazio. A pergunta 13 pergunta quem deve revisar.
