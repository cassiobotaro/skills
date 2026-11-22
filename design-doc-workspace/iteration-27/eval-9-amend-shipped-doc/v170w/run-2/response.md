Como o design doc já estava em produção, não reescrevi o corpo dele. Criei um mini-doc novo para a mudança e liguei os dois documentos, como a skill `design-doc` manda para sistemas que já foram ao ar.

- **Novo:** `docs/design/armazenamento-de-exportacoes-em-s3.md`. Segue a estrutura do original (header, visão geral, objetivos, solução, trade-offs, alternativas, questões em aberto) e tem uma seção de contexto a mais.
- **Original:** só o header mudou. A *Última atualização* agora é 2026-11-22 e entrou a linha *Alterado por*. O corpo ficou como estava.
- **Conteúdo do novo doc:** só o que você disse. Os arquivos saíram do disco do worker para um bucket S3. O motivo foi o segundo worker, que fazia o download cair em quem não tinha o arquivo e devolver 404. Também registrei que o doc original já havia descartado o bucket por assumir um único worker.
- **Autores e revisores:** estão como "A confirmar".
- **Perguntas:** ficaram as 10 que não consegui responder sozinha. As principais:
  - A data em que a mudança foi para produção.
  - Quem serve o download hoje (o worker, a API ou uma URL pré-assinada do S3).
  - Como funciona a retenção de 7 dias agora.
  - Como o worker se autentica no bucket e quem é o dono dele.
  - O que aconteceu com os arquivos antigos e com os links de download deles.
  - Qual custo o time aceitou com a mudança.
  - Se avaliaram outras saídas além do bucket, como roteamento por worker ou volume compartilhado.
  - Quem fora do time de Relatórios foi impactado.

Não afirmei nada que dependa dessas respostas. Por exemplo, o doc não diz que "qualquer worker serve o download" nem que a retenção continua em 7 dias. A seção de trade-offs só tem a vantagem que você descreveu, e o custo aceito depende da pergunta 7. Aplicadas as passadas de `technical-writing` e `unslop`. Não rodei nada nem commitei.
