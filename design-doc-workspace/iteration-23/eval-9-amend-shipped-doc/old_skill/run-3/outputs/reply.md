O design doc original está em produção (estado "Implementado", e você confirmou que roda desde março), então não reescrevi o corpo dele. Ele é o registro de por que o sistema nasceu assim, e continua correto sobre o que foi decidido na época. Fiz duas coisas:

1. **Novo mini-doc:** `docs/design/exportacao-de-relatorios-armazenamento-s3.md`. Ele nomeia o original, registra a mudança (disco local do worker para bucket S3) e o motivo (o segundo worker e o 404 no download), e traz trade-offs e alternativas só com o que você me disse.
2. **Original, só o cabeçalho:** `docs/design/exportacao-de-relatorios.md` ganhou a linha "Alterado por", com o link para o novo doc, e a "Última atualização" passou para 2026-11-16. O corpo ficou intacto.

Deixei como questões em aberto no novo doc o que eu não quis supor. Me responda e eu fecho o documento:

1. Em que data a mudança foi para produção?
2. Quem serve o download agora: o worker, a API ou um link direto do bucket? O endpoint `GET /exports/<job_id>/download` mudou?
3. A retenção de 7 dias continua? Se sim, quem a aplica agora: o cron do worker ou uma regra do bucket?
4. O que aconteceu com os arquivos que estavam no disco dos workers: houve migração ou eles expiram?
5. Quais custos o time aceitou com o bucket (dinheiro, latência, credenciais, acesso aos arquivos)? Hoje a seção de trade-offs só tem o ganho e a dependência nova, e um design sem custo nenhum é sinal de alerta.
6. Além de manter o disco local, o time considerou outra saída, como rotear o download para o worker que tem o arquivo?
