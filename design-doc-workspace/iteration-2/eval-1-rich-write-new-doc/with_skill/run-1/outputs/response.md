Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`.

Aproveitei tudo que você já trouxe (o prompt estava bem completo), então fui direto para a
escrita em vez de ficar perguntando. O que ficou no documento:

- **Problema e contexto** com os números que você deu: geração síncrona na request, timeout
  de 30s no gateway, ~12% de falhas acima de 50 mil linhas e ticket de suporte toda semana.
- **Objetivos mensuráveis**: zerar timeouts (tirando a geração do ciclo de request) e
  suportar 100 mil linhas (via streaming no worker).
- **A solução** com diagrama de arquitetura (API → RabbitMQ → worker → S3 → e-mail) e
  diagrama de sequência do fluxo completo, cada um seguido de explicação. Inclui uma seção
  de dados/sensibilidade por causa da PII.
- **Trade-offs explícitos**: o custo central que vocês aceitaram — perder o download imediato
  inclusive para exportações pequenas, em troca de um caminho único — está escrito sem
  maquiagem, junto com mais partes móveis, dependência da fila compartilhada e PII em e-mail.
- **Alternativas** numa tabela com trade-offs: timeout maior (descartada — só adia), BI
  externo (descartada — custo + PII a terceiro) e "não fazer nada" (descartada — sintomas
  persistem). A escolhida está marcada.
- **Cross-cutting concerns** para Plataforma (fila compartilhada) e Segurança (link assinado
  com PII), ambos sugeridos como revisores.
- Glossário, testabilidade/observabilidade, plano de implantação faseado e questões em aberto.

Um detalhe: os diagramas estão em Mermaid (renderizam direto no GitHub/GitLab), mas o
servidor de validação retornou erro de transporte, então não consegui validá-los por
ferramenta — são sintaxe Mermaid padrão e devem renderizar normalmente.

Deixei como **questões em aberto** (não inventei nada): autores e revisores nomeados, o TTL
do link assinado, qual serviço de e-mail e o tratamento de falha de entrega, a política de
retry/dead-letter da fila, a retenção dos arquivos no S3 e o que acontece quando o link
expira antes do download. Se você me passar essas respostas (principalmente autores/revisores
e o TTL combinado com Segurança), eu incorporo no corpo do doc e atualizo o estado.
