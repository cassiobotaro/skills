Criei o design doc em `docs/design/background-report-export-service.md`. Como a pasta `docs/design/` estava vazia (sem template nem outros docs pra seguir), usei o catálogo padrão de seções, mantendo só as que esse problema pede.

O documento foi escrito em torno dos trade-offs, que é o que dá valor de longo prazo a um design doc:

- **Problema e contexto** — geração síncrona estourando o timeout de 30s do gateway, 12% de falha acima de 50k linhas e os tickets semanais.
- **Objetivos mensuráveis** — zerar os timeouts (tirando a geração do caminho da request) e aguentar 100k linhas (streaming no worker).
- **A solução** — API enfileira no RabbitMQ e responde `202`; worker gera CSV/XLSX em streaming pro S3 e manda link assinado por e-mail. Tem um diagrama de arquitetura (estilo C4 container) e um de sequência do fluxo, cada um seguido de texto.
- **Trade-off central, explícito** — a perda do download imediato (exportação pequena também vira assíncrona) aceita em troca de um caminho único. Listei os custos sem maquiar: mais partes móveis, nova superfície de PII e dependência da entrega de e-mail.
- **Alternativas** — síncrono com timeout maior, BI externa e "não fazer nada", cada uma com o porquê de ter perdido, numa tabela com marcadores ✓/✗/⚠.
- **Cross-cutting** — Segurança (link assinado com PII, TTL, retenção) e Plataforma (fila compartilhada, dimensionamento). Sugeri os dois times como revisores.

Não inventei nada que você não estabeleceu. Deixei como **questões em aberto** (e gostaria da sua resposta pra fechar o doc):

1. **Autores e revisores** — pode me passar os nomes? Deixei o cabeçalho com placeholders.
2. **TTL do link assinado** — qual prazo de validade é aceitável pra Segurança?
3. **Retenção no S3** — por quanto tempo manter os arquivos com PII antes de apagar?
4. **Consumidores atuais da API** — quem chama `POST /exports` hoje esperando o arquivo na resposta? O contrato muda pra `202`, então é uma quebra de compatibilidade que precisa de plano de migração.
5. **Reexecução pelo usuário** — se cair na DLQ, o usuário consegue disparar de novo ou só via suporte?

Dois apontamentos:

- O diagrama de sequência inclui retentativas/DLQ e ack só após persistir/notificar como mecanismo natural da fila — se o comportamento desejado for outro, me avisa que ajusto.
- O servidor de validação de diagramas estava fora no momento, então os Mermaid não foram validados por máquina; a sintaxe é padrão e renderiza no GitHub/GitLab.
