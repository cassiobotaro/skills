Como o design doc original já está em produção desde março, não mexi no corpo dele. Ele é o registro de por que o serviço foi construído daquele jeito. Fiz duas coisas:

1. Criei `docs/design/exportacao-de-relatorios-armazenamento-s3.md`, um mini-doc que nomeia o original, diz o que mudou (arquivos saíram do disco do worker e foram para um bucket S3) e por quê (com o segundo worker, o download caía no worker sem o arquivo e devolvia 404).
2. No original, só o cabeçalho mudou: a linha **Alterado por**, com o link para o novo doc, e a **Última atualização** (2026-11-16). O novo doc também aponta de volta para o original.

Escrevi só o que você me contou. O resto ficou em "Questões em aberto" no novo doc, para você responder. Depois eu incorporo as respostas ao corpo:

- Quando a mudança entrou em produção?
- Quem serve o download agora (API, worker ou link direto do bucket) e como o acesso é controlado?
- Como ficam a retenção de 7 dias e o cron que apagava os arquivos do disco?
- Quais custos o time aceitou (credenciais, retenção, custo de storage e transferência, latência)? Hoje a seção de trade-offs só tem o ganho. Um doc sem custo declarado perde o valor.
- Os arquivos que estavam nos discos locais foram migrados ou descartados?
- O time considerou outras saídas, como disco compartilhado ou rotear o download para o worker de origem? Por que perderam?
- Quem deve revisar o doc? Deixei "A definir" no cabeçalho.
