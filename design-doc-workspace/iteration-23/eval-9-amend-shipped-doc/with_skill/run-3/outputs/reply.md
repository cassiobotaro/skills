Como o serviço está em produção desde março, não mexi no corpo do design doc original: ele é o registro de por que o sistema foi construído daquele jeito. Fiz duas coisas:

1. Criei `docs/design/armazenamento-de-arquivos-de-exportacao.md`, um mini-doc que aponta para o original, descreve o problema (segundo worker, download caindo no worker sem o arquivo e devolvendo 404) e a mudança (arquivos do disco local para um bucket S3).
2. No `docs/design/exportacao-de-relatorios.md`, só o cabeçalho mudou: `Última atualização` agora é 2026-11-16 e entrou a linha `Alterado por`, com link para o mini-doc.

O mini-doc só afirma o que você contou. Ficou como questões em aberto, e preciso das respostas para fechá-las:

- Quando a mudança entrou em produção?
- Qual custo o time aceitou com o bucket (credenciais, retenção, custo de storage e transferência, latência)? Hoje a seção de trade-offs tem só o ganho e a menção ao custo que o doc original previa.
- Quem serve o download agora: o worker lendo do S3 ou outro caminho?
- A retenção de 7 dias e o cron de limpeza do worker continuam valendo, ou a retenção passou para o bucket?
- O que aconteceu com os arquivos que estavam no disco dos workers na hora da troca?
- Além de "não fazer nada", que outras alternativas vocês avaliaram (por exemplo, direcionar o download ao worker que gerou o arquivo)?
- Quem revisa o mini-doc?
