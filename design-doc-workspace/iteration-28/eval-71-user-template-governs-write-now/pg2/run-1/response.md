Salvei o design doc em `docs/design/DD-2026-001-servico-de-deduplicacao-de-eventos.md`. Segui as seções do template na ordem, e as perguntas ficaram no final.

Fiz três escolhas que você deve conferir:
- **Alternativas:** o template não tem seção para elas. Coloquei as duas que você descartou e "não fazer nada" como subseção dentro de **Proposta**, junto com o trade-off dos +5 ms. Se o time de arquitetura não aceitar isso, é só mover o trecho.
- **Diagrama:** o diagrama de sequência (Mermaid) mostra só o que você descreveu: ingestor, serviço, Redis (chave por 24h) e Kafka, com descarte quando a chave já existe. Não coloquei nenhum detalhe que você não deu.
- **Número do documento:** `docs/design/` só tinha o `TEMPLATE.md`, então assumi DD-2026-001. Revisores ficou em branco.

O documento tem três lacunas que só você consegue preencher:
- **Plano de rollout:** você não me deu fases nem critérios de avanço ou rollback. A seção só aponta para as perguntas.
- **Riscos:** só o salto de latência tem mitigação. Registrei também a dependência do Redis na ingestão e a janela de 24h, que decorrem direto do desenho. A mitigação dos dois ficou como pergunta.
- **Perguntas abertas:** são 13, e as mais importantes são estas:
  - O que o serviço faz se o Redis cair: publica sem deduplicar ou rejeita o evento?
  - Duplicatas depois de 24h são aceitáveis?
  - Quem define a chave idempotente?
  - Os +5 ms são o esperado ou o teto?

Não rodei `claude plugin validate` nem `scripts/validate.py`, porque a mudança não toca nenhum `skills/`. Também não commitei nada.
