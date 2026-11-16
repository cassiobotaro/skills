O design doc original já estava aprovado e o serviço está em produção, então não reescrevi o corpo dele. Ele agora é o registro de por que o sistema foi construído daquele jeito (com um único worker e disco local). Fiz assim:

- **Novo mini-doc:** `docs/design/exportacao-de-relatorios-armazenamento-s3.md`, em rascunho. Ele aponta para o original, registra a mudança (disco local para bucket S3) e o motivo (o segundo worker fazia o download cair no worker sem o arquivo e devolver 404). Também registra o trade-off que o original já apontava: o bucket exige credenciais e política de retenção novas.
- **Original:** só o cabeçalho mudou. Adicionei a linha "Alterado por", com o link para o novo doc, e atualizei a "Última atualização" para 2026-11-16.

Não inventei o que você não me contou. Esses pontos estão em "Questões em aberto" no mini-doc e precisam da sua resposta:

1. Quando a mudança entrou em produção?
2. Como o download funciona agora? A API ou o worker lê do bucket e devolve o arquivo, ou o usuário recebe um link direto para o bucket? O contrato do endpoint mudou?
3. A retenção de 7 dias continua? Como ela é aplicada no bucket?
4. O que aconteceu com os arquivos que estavam no disco do worker?
5. Que custo ou risco o time aceitou (armazenamento, credenciais, dependência do S3)?
6. O time considerou outras saídas, como direcionar o download ao worker que gerou o arquivo ou usar disco compartilhado? Por que perderam?
7. Quem fora do time é afetado (Plataforma/Infraestrutura, Segurança) e quem deve revisar?

Com as respostas, eu complemento o doc e passo o estado para a revisão.
