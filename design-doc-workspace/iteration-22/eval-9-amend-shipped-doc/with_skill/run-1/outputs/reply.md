O design doc já está em produção, então não mexi no corpo dele. Ele é o registro de por que o serviço foi construído daquele jeito. Fiz duas coisas:

1. **Novo mini-doc** `docs/design/exportacao-de-relatorios-armazenamento-s3.md` (rascunho). Ele registra que os arquivos saíram do disco do worker e foram para um bucket S3. O motivo é o segundo worker: o download caía no worker que não tinha o arquivo e devolvia 404. Ele também aponta que isso derrubou a premissa de "um único worker" que o doc original listava como custo aceito. Retomei a alternativa do bucket que o original tinha descartado.
2. **Doc original**: só duas linhas no cabeçalho, `Amended by` apontando para o mini-doc e *Última atualização* = 2026-11-16.

Não inventei o que você não me contou. O mini-doc deixa estas perguntas em aberto, e preciso das respostas para fechá-lo:

1. Quando a mudança entrou em produção (data)?
2. Como o download funciona hoje? Quem serve o arquivo, e o endpoint `GET /exports/<job_id>/download` continua o mesmo?
3. Qual é a retenção no bucket? Os 7 dias e o cron de limpeza do worker continuam, ou a expiração passou para o bucket?
4. Que custos vocês aceitaram com a mudança (storage, credenciais, nova dependência, latência)? Hoje a seção de trade-offs não tem nenhum custo, e isso é um sinal de alerta.
5. Vocês avaliaram outras alternativas além do bucket (por exemplo, rotear o download para o worker dono do arquivo, ou usar disco compartilhado)?
6. Os arquivos que estavam nos discos dos workers foram migrados ou descartados?
7. Quem são os autores e revisores do mini-doc?
