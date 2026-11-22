Como o serviço já está em produção, o `docs/design/exportacao-de-relatorios.md` passa a ser o registro de por que ele foi construído daquele jeito. Pela skill `design-doc`, eu não reescrevo o corpo dele. Vou criar um mini-doc de emenda, `docs/design/exportacao-de-relatorios-bucket-s3.md`. Ele nomeia o original, explica o que mudou e por quê, e traz os próprios trade-offs. No original eu só acrescento a linha `Amended by` no cabeçalho e atualizo a *Última atualização*.

O motivo você já deu: com o segundo worker, o download caía no worker sem o arquivo e devolvia 404. O resto eu não encontrei no repositório e não vou inventar. Preciso destas respostas:

1. **Quando a mudança entrou em produção?** Preciso da data para o cabeçalho e para a *Última atualização* do original.
2. **Como o download funciona agora?** O worker lê do bucket e devolve o arquivo, ou o endpoint `GET /exports/<job_id>/download` redireciona para uma URL pré-assinada? Qualquer worker atende o download?
3. **Como ficou a retenção de 7 dias?** O cron do worker apaga os objetos do bucket, ou uma lifecycle rule do bucket faz isso? Os 7 dias continuam?
4. **O que mudou em credenciais, custo e operação?** O design original citava credenciais e política de retenção novas como custo do bucket. Quem gerencia isso (nome do bucket, role/credencial do worker)? Há custo de transferência ou de storage que valha registrar? E os arquivos que ficaram no disco local (`/var/exports`) na migração: foram migrados, descartados ou expiraram?

Se preferir, posso escrever agora o que já está estabelecido, com um `TODO` em cada lacuna, e você preenche depois.
