Como o serviço está em produção desde março, não reescrevi o design doc original. Escrevi um mini-doc novo e liguei os dois.

- **Novo:** `docs/design/exportacao-de-relatorios-armazenamento-s3.md`. Tem o contexto (segundo worker, 404 no download), a mudança (disco local para bucket S3), os trade-offs, as alternativas (incluindo "não fazer nada") e as questões em aberto. Passei `technical-writing` e `unslop` na prosa.
- **Original:** só o cabeçalho mudou. Entrou a linha `Alterado por` apontando para o novo doc, e `Última atualização` foi para 2026-11-22. O corpo está intacto.

Só escrevi o que você me disse e o que o repositório já registrava. Como você não pôde responder, deixei oito perguntas no fim do doc, e nenhuma seção afirma o que elas perguntam:

1. Quando o segundo worker subiu e quando os arquivos foram para o S3? Os arquivos antigos de `/var/exports` foram migrados ou descartados?
2. Como o download funciona agora? O worker lê do bucket ou o usuário baixa direto do S3? O endpoint mudou?
3. Os arquivos ainda ficam 7 dias? Quem apaga os antigos agora: o cron do worker ou uma regra do bucket?
4. Quem cuida das credenciais e do acesso ao bucket?
5. Que custo o time aceitou? Só consegui registrar a nova dependência do S3.
6. O risco de perder arquivos com o disco do worker deixa de existir?
7. Houve outras alternativas além do bucket, como direcionar o download ao worker que gerou o arquivo ou usar um volume compartilhado?
8. Quem revisa o doc? A Marina Prado revisou o original. O campo Revisores ficou "A definir", e Autores ficou "Time de Relatórios", como no original.

Quando você responder, é só me passar as respostas. Eu as incorporo ao corpo do doc e tiro as perguntas respondidas da lista.
