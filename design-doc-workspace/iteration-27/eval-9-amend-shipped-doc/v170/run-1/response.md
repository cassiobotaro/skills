Como o doc original já foi aprovado e está em produção, deixei o corpo dele como estava. Ele é o registro de por que o serviço foi construído daquele jeito. A mudança entrou como uma emenda curta.

- **Novo:** `docs/design/exportacao-de-relatorios-armazenamento-s3.md`. Ele conta o que mudou (disco local do worker para bucket S3), o motivo (o segundo worker fazia o download cair em quem não tinha o arquivo e devolver 404) e os trade-offs.
- **Original:** só o cabeçalho mudou, com uma linha `Emendado por` apontando para a emenda e a *Última atualização* em 2026-11-22. O link também aponta da emenda para o original.

Escrevi só o que você me contou. O que ficou de fora está em **Questões em aberto** na emenda, para você responder:

1. O download agora é servido pelo worker lendo do S3, ou por redirecionamento para uma URL do bucket?
2. A retenção de 7 dias continua? Se sim, quem a aplica agora: o cron do worker ou uma regra de ciclo de vida do bucket?
3. O que aconteceu com os arquivos que estavam no disco quando a mudança entrou?
4. Quem são os autores e revisores da emenda? Deixei o campo de autores fora do cabeçalho.

Também não registrei a data em que a mudança foi para produção. Se você me passar essas respostas, eu preencho a emenda e removo as perguntas.
