Escrevi o rascunho do design doc em `docs/design/servico-webhooks-saida.md`, com a arquitetura (contêineres em Structurizr DSL, com o código-fonte dobrado num bloco `<details>`) e o fluxo de entrega com reenvio (diagrama de sequência em Mermaid).

O que ficou de fora por falta de informação, e que precisa de você antes de virar versão final:

1. **Assinatura HMAC**: qual algoritmo, qual cabeçalho, e como o segredo de cada cliente é criado, entregue e trocado.
2. **Aceite**: quais respostas do endpoint do cliente contam como evento entregue.
3. **DLQ**: onde ela fica (tópico Kafka, tabela ou outro) e quem trata os eventos que chegam nela.
4. **Idempotência e ordem**: o cliente pode receber o mesmo evento mais de uma vez? A ordem por cliente é preservada?
5. **Migração e custos**: os serviços que fazem POST manual hoje vão migrar para o novo serviço, e em que ordem? Além do atraso na entrega, que outro custo o time aceitou?

Também faltam os autores, os revisores, o plano de entrega e a forma de medir "nenhum evento perdido". Esses itens estão na seção de perguntas em aberto do documento.

A imagem do diagrama de contêineres é uma referência de placeholder (`diagrams/servico-webhooks-conteineres.svg`). Nesta máquina não há Docker nem CLI do Structurizr, então ela precisa ser renderizada na revisão manual, a partir do código-fonte que está no próprio documento.
