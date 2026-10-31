Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`, com o diagrama de contêineres renderizado em `docs/design/diagrams/Containers.svg` (mais a legenda e a visão de contexto na mesma pasta).

O que o documento traz, a partir do que você descreveu: o contexto (geração na request, timeout de 30 s no gateway, 12% de falha acima de 50 mil linhas, tickets semanais), os dois objetivos (zerar timeouts e sustentar 100 mil linhas), a solução em quatro contêineres (API, fila no RabbitMQ, worker, bucket no S3) mais o e-mail com link assinado, o fluxo em diagrama de sequência, os trade-offs com o custo aceito (perda do download imediato em troca do caminho único), as três alternativas descartadas mais "não fazer nada", e uma seção de preocupações transversais com um parágrafo para Plataforma e um para Segurança, que também entram como revisores no cabeçalho.

Validação: o DSL do diagrama C4 passou no `structurizr validate` e foi exportado para SVG com a imagem `structurizr/structurizr:2026.10.26-playwright`; o diagrama de sequência Mermaid passou no `minlag/mermaid-cli`. O `inspect` do Structurizr aponta que API e worker estão sem tecnologia e as setas sem protocolo. Deixei assim de propósito: você não disse qual stack roda a API e o worker, e preferi deixar o slot vazio a inventar.

Registrei dez questões em aberto no fim do doc. Quatro delas fariam mais diferença se você responder agora, que eu já incorporo:

1. De onde o worker lê os dados do relatório? É a mesma base que a API usa hoje? Isso entra no diagrama como um contêiner a mais.
2. O que a API responde ao usuário depois de enfileirar o job, e ele tem como acompanhar o estado da exportação enquanto o e-mail não chega?
3. O que acontece quando a geração, o upload ou o e-mail falham: retentativa, aviso ao usuário, os dois? Hoje o fluxo desenhado é só o caminho feliz.
4. Validade do link assinado e retenção do arquivo no S3 já têm uma proposta sua, ou isso fica para o time de Segurança definir?

Também faltam os nomes de autor e dos revisores de Plataforma e Segurança no cabeçalho.
