Salvei o documento em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Não é commit, só o arquivo no disco.

Segui o `TEMPLATE.md` na ordem das seções: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.

- **Seção extra:** o template não tem lugar para as alternativas que vocês discutiram. Criei "Alternativas consideradas" entre Proposta e Riscos, com as duas descartadas e "não mudar nada", e avisei no próprio texto que ela não é do template. Se a arquitetura recusar seções fora do template, mova esse conteúdo para dentro de Proposta.
- **Diagrama:** pus um diagrama de sequência em Mermaid na Proposta (ingestor, serviço, Redis, Kafka). Não pus protocolos nem tecnologias que você não citou.
- **Numeração:** não havia outros docs em `docs/design/`, então usei DD-2026-001 e 2026-11-23 como data. A pergunta 13 pede que você confirme.
- **Riscos e rollout:** você só deu um risco, os +5 ms no caminho crítico, e só ele está na seção. Rollout só aponta para as perguntas abertas. Não inventei mitigações nem fases.
- **Revisores:** deixei em branco.

As 13 perguntas abertas estão no final. As que mais pesam no desenho:
- **Falha do Redis:** o serviço deixa passar ou bloqueia?
- **Ordem entre registrar a chave e publicar no Kafka:** se a publicação falhar depois do registro, o retry do produtor vira "duplicata" e o evento se perde.
- **Janela de 24h:** ela cobre o maior retry dos produtores?
- **Chave idempotente:** quem a gera?
