Rafael, o doc está em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`, seguindo o `TEMPLATE.md` na ordem: cabeçalho, Motivação, Proposta, Riscos, Métricas de sucesso e Perguntas abertas.

**Desvio do template.** O template não tem lugar para as alternativas que vocês discutiram, então acrescentei "Alternativas consideradas" como subseção da Proposta, sem mexer na ordem das seções do template. Inclui "não fazer nada", escrito só a partir da dor que você descreveu (4% de duplicatas, faturamento inflado, duas reclamações do financeiro). Se o time de arquitetura não aceita nenhuma seção extra, mova esse conteúdo para a Proposta em prosa.

**Seções do template que ficaram de fora.** Cada uma está marcada como opcional ou como "apague se não se aplica", e você não me deu o que preencher:
- Histórias de usuário e Plano de rollout: opcionais, sem conteúdo informado.
- Critérios de aceite: só vale se o doc estiver ligado a uma história do backlog, e você não disse que está.
- Estratégia de migração: o template manda apagar se não houver dados a migrar, e você não informou isso. Se há dados a migrar, me diga e eu escrevo a seção.

Incluí Métricas de sucesso (também opcional) porque você deu a meta de duplicatas abaixo de 0,1%.

**O que ficou em aberto.** Não inventei nada além do que você disse. A seção Riscos traz só o salto extra no caminho crítico (+5ms estimado), sem mitigação. Pergunto na seção Perguntas abertas:
- Qual é a chave idempotente, e quem a gera?
- O que o serviço faz se o Redis cair (deixa passar ou bloqueia)?
- Quais são as mitigações e os outros riscos?
- Quem são os revisores? O campo ficou em branco.
- Há backlog ligado, dados a migrar ou plano de rollout?

**Pontos para conferir.**
- O ID `DD-2026-001` supõe que esta é a primeira entrada da coleção, porque só o `TEMPLATE.md` existe em `docs/design/`. Ajuste se houver docs em outro lugar.
- O diagrama C4 tem o código Structurizr DSL dobrado em `<details>`, sem tecnologia no Ingestor nem nos produtores, porque você não informou. A imagem `diagrams/architecture.svg` é um placeholder, com uma nota para renderizar no passe manual. Não validei nem renderizei o DSL, porque não rodei Docker.
- A data (2026-11-16) é a de hoje.
