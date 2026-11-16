Como o serviço já está em produção, não mexi no corpo do `docs/design/exportacao-de-relatorios.md`. Ele registra por que o sistema foi construído daquele jeito. Fiz duas coisas:

1. Criei `docs/design/exportacao-de-relatorios-armazenamento-s3.md`, um mini-doc que diz o que mudou (disco local do worker para bucket S3), o motivo (o segundo worker e o 404 no download) e a alternativa "não fazer nada".
2. No doc original, só o cabeçalho mudou: adicionei a linha "Alterado por", com link para o novo doc, e atualizei a "Última atualização" para 2026-11-16. O novo doc aponta de volta para o original.

Não escrevi o que você não me contou. Ficou como questão em aberto no novo doc, e preciso das respostas:

- Quando a mudança entrou em produção?
- Quem serve o `GET /exports/<job_id>/download` hoje e como entrega o arquivo?
- Como funciona a retenção agora? O original previa 7 dias, com um cron do worker.
- O que aconteceu com os arquivos que estavam no disco dos workers?
- Que outras alternativas vocês pesaram para o 404 (por exemplo, um volume compartilhado) e por que o bucket venceu?
- O que essa abordagem piora e o que vocês decidiram aceitar (custo, dependência nova, credenciais, latência)?

Com as respostas eu preencho o trade-offs e as alternativas no novo doc.
