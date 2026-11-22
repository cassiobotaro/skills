O design doc está em produção (estado "Implementado", e você confirmou). Por isso não vou reescrever o corpo dele. Ele é o registro de por que o serviço nasceu com disco local. A mudança vai num mini-doc novo que cita o original e explica a mudança e o motivo. No original, a única edição é uma linha `Amended by` no cabeçalho e a *Última atualização*.

Já tenho o motivo: com dois workers, o download caía no worker sem o arquivo e devolvia 404. Antes de escrever, preciso de alguns dados que o repositório não tem e que não vou inventar:

1. **Quando** a mudança entrou em produção? Preciso da data para o cabeçalho do mini-doc e para a *Última atualização* do original.
2. **Quem serve o download agora?** `GET /exports/<job_id>/download` continua passando pelo worker, que lê do S3, ou a API redireciona para uma URL pré-assinada? Se for URL pré-assinada, qual a validade?
3. **Retenção:** os 7 dias e o cron que apagava os arquivos viraram uma lifecycle rule do bucket, ou o cron continua apagando objetos? Isso fecha o trade-off antigo "se o disco se perde, os arquivos se perdem".
4. **Detalhes do bucket:** qual o nome e o prefixo das chaves (ainda `<job_id>.csv`)? Como o worker se autentica (role ou credenciais)? Quem aprovou ou revisou a mudança?

Se preferir que eu escreva já, deixo `TODO` onde faltar informação. Diga e eu faço assim.
