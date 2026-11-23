Escrevi o documento em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Não commitei nada.

O doc segue as seis seções do `TEMPLATE.md`, na ordem do template. Só usei o que você me disse e deixei o resto como pergunta.

**Desvios do template**
- Adicionei **Alternativas consideradas** como subseção de Proposta. Você descreveu duas alternativas e o trade-off aceito, e o template não tem onde guardá-los. Se a arquitetura preferir esse conteúdo em outro lugar, é fácil mover.
- Escolhi o ID **DD-2026-001** porque `docs/design/` só tinha o template. Confirme a sequência.

**Seções que ficaram quase vazias, de propósito**
- **Riscos** tem só o +5ms de latência, que você já aceitou. Não inventei outros riscos nem mitigações.
- **Plano de rollout** diz apenas que ainda não foi definido. Você não deu fases nem critérios de avanço ou rollback.
- **Revisores** ficou "A definir".

**Perguntas abertas no final (8)**
1. Quem revisa o documento.
2. Quem gera a chave idempotente e como.
3. Por que 24h, e o que acontece com reenvios depois da janela.
4. Outros riscos, mitigação do +5ms e de onde vem essa estimativa.
5. Fases do rollout e critérios de avanço e de rollback.
6. Como medir a taxa de duplicatas e em que prazo chegar a 0,1%.
7. Se "não fazer nada" foi discutida.
8. Se a numeração DD-2026-001 está certa.

O doc tem um diagrama simples em Mermaid com os componentes que você citou (produtores, ingestor, serviço, Redis, Kafka). Ele não mostra tecnologia nem protocolo nas setas, porque você não os informou.
