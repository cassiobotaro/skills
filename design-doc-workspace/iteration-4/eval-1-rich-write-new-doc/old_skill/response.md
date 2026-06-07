Pronto! Como você já trouxe o problema, a solução, as alternativas e os times impactados, escrevi o doc direto, sem ficar te interrogando. Salvei em:

`docs/design/exportacao-de-relatorios-em-background.md`

O que tem nele:

- **Visão geral + contexto** — só o cenário de hoje (geração síncrona na request, timeout de 30s no gateway, ~12% de falha acima de 50 mil linhas, tickets semanais). Sem solução nem objetivo vazando pro contexto.
- **Objetivos mensuráveis** — zerar timeouts, aguentar 100 mil linhas e unificar num caminho só. Fora de escopo deixa explícito que o download imediato deixa de existir.
- **A solução em seções** — visão geral, um diagrama de containers (C4), um diagrama de sequência do fluxo (enfileirar → gerar em streaming → S3 → link assinado → e-mail), o estado do job e a sensibilidade do dado (PII justificando o link assinado). Cada diagrama vem seguido de texto explicando os componentes.
- **Trade-offs** — com os ✗ na cara: perda do download imediato (a contrapartida que vocês aceitaram), mais partes móveis, dependência do e-mail e a nova superfície de PII por link.
- **Alternativas** — tabela com a proposta, o síncrono com timeout maior, a ferramenta de BI externa e o "não fazer nada", cada uma com o motivo de ter perdido.
- **Concerns transversais** — Plataforma (fila compartilhada) e Segurança (link assinado com PII), sugeridos como revisores no header.
- **Testabilidade/observabilidade, plano de implantação faseado e questões em aberto**.

Dois detalhes pra você fechar:

1. Deixei **autores e revisores nominais** como placeholder no header — me diga os nomes (e quem de Plataforma/Segurança vai revisar) que eu preencho.
2. Os diagramas Mermaid foram escritos inline mas **não passaram por validação automática** (a ferramenta de validação não estava disponível no ambiente) — valem como ilustração; vale renderizar no GitHub/wiki pra conferir.

As **questões em aberto** que registrei (isolamento da fila no RabbitMQ, TTL do link e retenção no S3, política de retry/DLQ, e se o endpoint de status é necessário já no primeiro corte) são justamente os pontos que dependem de alinhamento com Plataforma e Segurança — quando vocês decidirem, eu incorporo no corpo do doc.
