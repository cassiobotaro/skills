Escrevi o rascunho do design doc do serviço de webhooks de saída em `docs/design/webhooks-saida.md`, dentro do repositório. Ele registra o que você já estabeleceu: o problema (entregas perdidas quando o endpoint do cliente cai, descobertas pelo suporte), a solução (serviço único que consome o Kafka, grava as tentativas no Postgres, envia o POST com HMAC e faz retry com backoff exponencial por até 24 horas, depois a DLQ), a alternativa descartada (SaaS, pelo custo por evento e pelo payload sair da nossa borda) e o trade-off aceito (entrega não imediata em alguns casos).

Os diagramas estão assim:
- Arquitetura: diagrama de containers em Structurizr DSL, com a referência à imagem como placeholder e o DSL dentro de um bloco `<details>`. Não tenho Docker nem a CLI do Structurizr aqui, então a imagem precisa ser gerada na passagem manual.
- Fluxo de entrega com retry: diagrama de sequência em Mermaid, dentro do documento. Onde você não definiu o mecanismo (como o agendamento é feito, o destino da DLQ, o critério de sucesso), deixei uma nota marcando-o como a definir, em vez de inventar.

Preciso de respostas para fechar estes pontos. Não consegui perguntar antes de escrever, então estão no documento como perguntas em aberto:

1. Qual a meta numérica dos objetivos? Por exemplo, por quanto tempo de indisponibilidade do cliente os eventos precisam ser cobertos, e qual percentual de entregas é esperado.
2. Você considerou outras alternativas além de não fazer nada e do SaaS? Se sim, quais e por que perderam?
3. A janela de 24 horas começa na criação do evento ou na primeira tentativa? E qual código de resposta conta como sucesso?
4. Se o serviço cair depois de enviar o POST e antes de gravar o sucesso, o cliente recebe o evento de novo? Se sim, os clientes precisam tratar eventos repetidos, e isso é um custo que o time aceita?
5. Onde ficam a DLQ e o agendamento das novas tentativas (tabela no Postgres, tópico no Kafka ou outro mecanismo)? E quem reprocessa a DLQ?
6. Como as chaves HMAC são provisionadas, guardadas e rotacionadas?

Ainda faltam os autores, os revisores (com a área de cada um), o escopo fora de escopo e a stack do serviço. Também não sei se a pasta `docs/design/` segue alguma convenção de nomes ou numeração no repositório, porque ele estava vazio. Se houver um template de design doc da casa, me envie a referência, porque ele passa a governar as seções.
