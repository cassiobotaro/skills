Como o serviço já está em produção, o design doc original virou o registro de por que o sistema foi construído daquele jeito. Por isso não reescrevi o corpo dele. Fiz duas coisas:

1. Criei `docs/design/exportacao-de-relatorios-armazenamento-s3.md`, um mini-doc que registra a mudança. Ele diz que os arquivos saíram do disco local do worker e foram para um bucket S3, e que o motivo foi o segundo worker devolvendo 404 no download. Também traz os trade-offs que o próprio doc original já tinha apontado: o fim da dependência do disco e a perda de arquivos junto com ele, de um lado, e a dependência de object storage, credenciais e retenção, do outro.
2. No original, mudei só o cabeçalho. Atualizei a "Última atualização" para 2026-11-16 e acrescentei a linha "Alterado por", com o link para o novo doc. O novo doc linka de volta para o original.

Não inventei nada além do que você me contou. Deixei estas perguntas em "Questões em aberto" no novo doc, e preciso das respostas para fechá-lo:

- O que mais ficou pior com o bucket (latência, custo, permissões)?
- A retenção de 7 dias continua? Quem a aplica agora, o cron do worker ou uma regra de lifecycle do bucket?
- O download ainda passa pelo worker ou o cliente recebe uma URL do bucket?
- Os arquivos antigos do disco foram migrados ou descartados?
- Vocês consideraram outra alternativa além do bucket (disco compartilhado, roteamento ao worker de origem)?
