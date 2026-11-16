Como o serviço já está em produção, não reescrevi o design doc original: ele é o registro de por que o sistema foi construído daquele jeito. A mudança ficou num documento novo, uma emenda curta, ligada ao original nos dois sentidos.

O que fiz:

- **Novo:** `docs/design/exportacao-de-relatorios-arquivos-no-s3.md`. Segue a mesma estrutura do original e registra o que mudou (disco local do worker para bucket S3) e o motivo (segundo worker, download caindo no worker sem o arquivo, 404).
- **Original:** `docs/design/exportacao-de-relatorios.md` ganhou só a linha **Emendado por** no cabeçalho e a **Última atualização** passou para 2026-11-16. O corpo ficou intacto, inclusive o trecho que diz que a solução assume um único worker.

Na emenda, os trade-offs e as alternativas vêm só do que você me contou e do que o documento original já dizia: o S3 era a alternativa descartada lá por exigir credenciais e política de retenção novas, e o disco local tinha como vantagens não trazer dependência nova e não ter custo de transferência de storage externo. Não inventei o resto. O que falta está na seção "Questões em aberto" da emenda, e preciso das suas respostas para fechar:

1. Como o `GET /exports/<job_id>/download` entrega o arquivo agora?
2. Como funciona a retenção de 7 dias agora que o arquivo não está mais no disco do worker (antes era um cron do worker)? O prazo continua o mesmo?
3. O que aconteceu com os arquivos que já estavam no disco dos workers no momento da mudança?
4. Quais custos o time aceitou ao ir para o S3, além dos que o documento original já previa?
5. Vocês avaliaram outras alternativas antes de escolher o S3? Quais, e por que perderam?
6. O que motivou subir o segundo worker?
7. O que ficou deliberadamente fora de escopo nesta mudança?
8. Quando a mudança entrou em produção?
9. Quem são os autores da emenda e quem a revisou? Deixei os dois campos do cabeçalho como "A confirmar".

Com as respostas eu incorporo cada uma na seção certa e tiro a questão da lista.
