O serviço já está em produção, então não vou reescrever o corpo do design doc. Ele é o registro de por que o sistema foi construído daquele jeito. O plano é:

1. Criar um mini-doc de emenda, `docs/design/exportacao-de-relatorios-armazenamento-s3.md`. Ele cita o original, diz o que mudou e por quê, e traz os próprios trade-offs.
2. Editar só o cabeçalho do original: adicionar a linha `Amended by` com o link e atualizar a *Última atualização*.

O motivo você já deu: o segundo worker fazia o download cair num worker sem o arquivo e devolver 404. Antes de escrever, preciso de alguns fatos que só você tem. Não quero inventá-los.

1. **Quando** a mudança entrou em produção? Preciso da data para a *Última atualização* e para o mini-doc.
2. **Como o download funciona agora?** O worker lê do S3 e devolve o arquivo, ou o endpoint `GET /exports/<job_id>/download` redireciona para uma URL pré-assinada? Se for pré-assinada, qual a validade?
3. **Retenção:** os 7 dias continuam? Quem apaga os arquivos agora: uma lifecycle rule do bucket ou o cron do worker?
4. **Credenciais e acesso:** como os workers acessam o bucket (role/IAM, chave)? O design original citava isso como custo da alternativa de object storage. Há algo a registrar, como nome do bucket, criptografia ou acesso restrito?
5. **Trade-offs reais:** além de resolver o 404 e de os arquivos não se perderem mais com o disco, vocês viram custos (transferência, latência, dependência do S3)? Ainda existe algum arquivo em `/var/exports` de antes da mudança, ou houve migração?
6. **Revisores/autores** do mini-doc: mantenho o Time de Relatórios como autor? Quer incluir a Marina Prado (Plataforma) como revisora?

Com as respostas eu escrevo o mini-doc e faço a edição no cabeçalho.
