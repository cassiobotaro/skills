O design doc já está em produção, então não vou reescrever o corpo dele. Ele registra por que o sistema foi construído daquele jeito, e reescrevê-lo apagaria esse raciocínio. O plano é este:

- **Documento novo:** um mini-doc em `docs/design/` que aponta para o original, conta o que mudou e por quê, e traz seus próprios trade-offs.
- **Edição no original:** só uma linha `Amended by` no cabeçalho, apontando para o novo, e a *Última atualização*.

Antes de escrever, preciso de algumas respostas. Não encontrei esses fatos no repositório e não quero inventá-los:

1. **Quando a mudança foi para produção?** Só sei que o serviço está em produção desde março.
2. **Como o download funciona hoje?** O endpoint `GET /exports/<job_id>/download` continua servido pelo worker, que lê do S3? Ou a API devolve um link do bucket (por exemplo, URL pré-assinada)? Qual dos dois workers atende?
3. **E a retenção de 7 dias?** O cron do worker foi substituído por uma lifecycle rule do bucket, ou o cron apaga objetos do S3?
4. **O que aconteceu com os arquivos antigos em `/var/exports`?** Houve migração, ou eles foram descartados?
5. **O que a mudança piorou ou custa agora?** O original cita credenciais e política de retenção novas como custo do bucket. Isso se confirmou? Há custo de storage ou de transferência, ou uma dependência nova que preocupe o time?
6. **Existe outra alternativa que o time pesou?** Por exemplo, afinidade de sessão no balanceador ou volume compartilhado entre os workers. "Não fazer nada" já tem motivo claro: o 404 intermitente no download. Só registro o que você confirmar.

Com as respostas, escrevo o mini-doc, rodo `technical-writing` e `unslop` nele e ajusto o cabeçalho do original.
