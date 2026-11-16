Atualizei `docs/design/exportacao-de-relatorios.md` com o que você contou. Só registrei o que você estabeleceu.

O que mudou no documento:

- **Solução:** o worker agora grava o arquivo num bucket S3. O texto mantém o desenho anterior (disco local, download servido pelo worker) como histórico e registra o motivo da mudança: com o segundo worker, o download caía no worker sem o arquivo e devolvia 404.
- **Trade-offs:** troquei os itens do desenho antigo pelos do novo. O ganho é que qualquer worker serve o download e os arquivos não dependem mais de um disco. O custo é a dependência nova do bucket. Deixei uma nota de que a premissa de worker único não se sustentou.
- **Alternativas:** "bucket de object storage" passou a constar como adotada em 2026-11-16, e "manter o disco local" entrou como a solução original abandonada.
- **Cabeçalho:** a última atualização agora é 2026-11-16. O estado continua "Implementado".

Preciso das respostas abaixo antes de preencher mais. Deixei as três em "Questões em aberto":

1. Por quanto tempo os arquivos ficam no bucket? Os 7 dias e o cron do worker continuam valendo, ou a retenção virou uma regra do bucket?
2. Quem serve o download agora: o worker lendo do bucket, ou a API devolvendo um link direto para o bucket?
3. Que outros custos o time aceitou, como storage, transferência e credenciais? Só listei a dependência nova.

Com essas respostas eu atualizo a Solução e os Trade-offs. Se o objetivo de 5 minutos ou o formato do download mudou, me avise também.
