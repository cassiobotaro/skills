Como o serviço já está em produção, não reescrevi o design doc original. Ele agora é o registro de por que o sistema foi construído com disco local, então o corpo dele ficou intacto. Fiz duas coisas:

1. Criei `docs/design/armazenamento-de-exportacoes-em-s3.md`, um mini-doc que referencia o original e registra o que mudou (disco local do worker para bucket S3) e por quê (com o segundo worker, o download caía no worker sem o arquivo e devolvia 404). Ele traz os trade-offs que você me deu e a alternativa "não fazer nada".
2. No original, `docs/design/exportacao-de-relatorios.md`, mudei só o cabeçalho: adicionei a linha "Alterado por" com o link para o novo doc e atualizei a "Última atualização" para 2026-11-16.

Não inventei nada além do que você contou. Ficaram como "Questões em aberto" no mini-doc, e preciso das suas respostas para fechar:

- Que custos o time aceitou com o bucket (credenciais, política de retenção, custo de storage e transferência)?
- A retenção de 7 dias e a limpeza que o cron do worker fazia continuam valendo, ou o bucket assumiu isso?
- Que outras alternativas o time considerou para o 404 além de não fazer nada?
- Quem deve revisar a mudança?
