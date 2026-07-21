Escrevi o design doc em `docs/design/exportacao-de-relatorios-em-background.md`, com o
diagrama de arquitetura renderizado em `docs/design/diagrams/arquitetura-exportacao.svg`.

Como o repositório ainda não tinha design docs, usei o catálogo padrão de seções e
selecionei as que o seu problema pedia: glossário, visão geral, escopo e contexto,
objetivos e fora de escopo, a solução (com arquitetura, fluxo e sensibilidade dos dados),
trade-offs, alternativas consideradas, preocupações transversais e perguntas em aberto.

O que o documento registra a partir do que você contou:

- **Contexto**: geração síncrona dentro da requisição, corte do gateway em 30 s, 12% de
  falha acima de 50 mil linhas, ticket semanal do suporte, RabbitMQ já em operação.
- **Objetivos medíveis**: zerar os timeouts e suportar 100 mil linhas, cada um nomeando o
  mecanismo (tirar a geração do caminho da requisição, gerar em streaming).
- **Trade-off aceito, escrito sem maquiagem**: o usuário perde o download imediato, e as
  exportações pequenas também viram assíncronas para existir um caminho só. Somei os
  custos que decorrem do desenho: mais peças no caminho, PII em repouso acessível por
  link enviado por e-mail e carga nova na fila compartilhada.
- **Alternativas**: síncrono com timeout maior, BI externo e — porque toda alternativa
  precisa dela — *não fazer nada*, refutada pelos 12% de falha e pelo ticket semanal.
- **Preocupações transversais**: uma subseção para Segurança (link assinado com PII), uma
  para Plataforma (fila compartilhada) e uma para Compatibilidade (o contrato da API muda
  para todos os consumidores).

Sobre os diagramas: a arquitetura foi escrita em Structurizr DSL (validado no servidor MCP
do Structurizr, retorno `OK`), exportada para PlantUML e renderizada em SVG — a imagem
está embutida no doc com a DSL dobrada logo abaixo, então quem editar o modelo acha a
fonte a um clique. O fluxo é um diagrama Mermaid, validado e renderizado
([abrir para editar](https://l.mermaid.ai/VXAFHE)); ele mostra só o caminho feliz, porque
você ainda não definiu o que acontece quando o worker falha — deixei isso registrado como
pergunta em aberto em vez de inventar um ramo de erro.

Ficaram alguns buracos que só você (ou o time) pode preencher — anotei todos em
*Perguntas em aberto* no documento, mas estes seis são os que mais mudam o desenho:

1. **Autoria e revisão**: quem assina o documento, e quais nomes de Plataforma e Segurança
   entram como revisores? Deixei os campos do cabeçalho como *a definir*.
2. **Estado do job**: o usuário consegue consultar o andamento da exportação, ou o e-mail
   é o único sinal de que terminou? Isso decide se entra um armazenamento de estado no
   desenho (hoje não desenhei nenhum, porque você não mencionou).
3. **Falha do worker**: retentativa, fila de mensagens mortas, aviso ao usuário — o que
   acontece quando a geração morre no meio?
4. **Link assinado**: qual a validade dele e por quanto tempo o arquivo fica retido no S3?
   É a primeira pergunta que Segurança vai fazer.
5. **Envio do e-mail**: qual serviço, e o worker chama direto ou publica em alguma fila de
   notificação que já existe?
6. **Verificação**: qual métrica prova que os timeouts foram a zero e que 100 mil linhas
   passam? Com a resposta, escrevo a seção de testabilidade e observabilidade — hoje ela
   não existe no doc.

Me responda o que quiser e eu incorporo direto no documento.
