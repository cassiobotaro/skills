Como o serviço já está em produção, o documento original virou o registro de por que o sistema foi construído daquele jeito. Por isso não reescrevi o corpo dele. Fiz o seguinte:

- `docs/design/exportacao-de-relatorios.md`: só o cabeçalho mudou. Adicionei a linha **Alterado por**, que aponta para o novo documento, e atualizei a **Última atualização** para 2026-11-16.
- `docs/design/exportacao-de-relatorios-armazenamento-s3.md` (novo, estado Rascunho): um mini-doc que cita o original e registra a mudança. Ele diz que o segundo worker fazia o download cair no worker sem o arquivo e devolver 404, e que por isso os arquivos foram para um bucket S3. Também traz "não fazer nada" como alternativa, escrita só com o problema que você descreveu.

Não escrevi nada que você não me contou, então faltam respostas para fechar o rascunho:

1. Quando a mudança foi para produção?
2. O que ela piorou ou encareceu, e o que o time aceitou (custo de storage, credenciais novas, dependência nova, latência)? Sem isso o doc não tem trade-offs, e é a parte mais importante dele.
3. Quem serve o download agora, e como o arquivo chega ao usuário?
4. A retenção de 7 dias e o cron de limpeza continuam valendo? Como?
5. Que outras alternativas o time avaliou além do S3 (por exemplo, direcionar o download ao worker certo, ou disco compartilhado)?
6. Quem assina o documento e quem deve revisar (Plataforma, Infraestrutura)?

Com as respostas, eu complemento o novo documento e tiro essas perguntas da lista de questões em aberto.
