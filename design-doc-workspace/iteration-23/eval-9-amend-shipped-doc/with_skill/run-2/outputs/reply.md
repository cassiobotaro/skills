Como o serviço já está em produção, não mexi no corpo de `docs/design/exportacao-de-relatorios.md`. Ele é o registro de por que o sistema nasceu com o disco local. Fiz duas coisas:

1. Criei `docs/design/exportacao-de-relatorios-armazenamento-s3.md`, um mini-doc que aponta para o original e registra a mudança (disco local do worker para bucket S3) e o motivo (o segundo worker fazia o download cair no worker sem o arquivo e devolver 404). A alternativa "bucket" que o original tinha descartado aparece nele como a escolhida.
2. No original, só editei o cabeçalho. Adicionei a linha `Alterado por`, com o link para o novo doc, e atualizei a `Última atualização` para 2026-11-16. O corpo continua igual, então quem ler o original chega à mudança pelo link.

Escrevi apenas o que você me disse. Preciso destas respostas para completar o mini-doc, que as lista em "Questões em aberto":

- Em que data os arquivos passaram a ir para o S3?
- Quem serve o download hoje: o worker, a API ou uma URL do próprio S3?
- Os 7 dias de retenção continuam valendo, e quem apaga os arquivos antigos agora (o cron do worker ou uma regra do bucket)?
- O que aconteceu com os arquivos que já estavam em `/var/exports` na migração?
- O que essa abordagem piora e o que o time decidiu aceitar (custo, latência, dependência do S3, credenciais)? Sem isso, a seção de trade-offs só lista os ganhos.
- Quem revisa a mudança?
