Escrevi o design doc do serviço de entrega de webhooks de saída em `docs/design/entrega-webhooks-saida.md`, dentro do repositório. Como não há outros design docs no repositório, usei o caminho que você indicou e a estrutura padrão do skill.

O documento traz o problema de hoje, a solução (serviço único que consome o Kafka, grava as tentativas no Postgres, envia POST assinado com HMAC e reenvia com backoff exponencial por até 24 horas, depois manda para a DLQ), o trade-off que você aceitou (entrega que deixa de ser imediata em alguns casos), e as alternativas: não fazer nada, descartada pela dor descrita, e o SaaS de webhooks, descartado pelo custo por evento e pelo payload fora da nossa borda. Também tem o fluxo de entrega com reenvio em Mermaid e o modelo C4 de contêineres em Structurizr DSL, dentro de um bloco de código.

Pontos que o documento não preenche porque você não os informou, e que estão em "Questões em aberto":

1. Qual é a medida de "nenhum evento perdido"?
2. Quais parâmetros do backoff (intervalo inicial, fator, limite, variação aleatória) e o que conta como entrega bem-sucedida (códigos de resposta, timeout)?
3. Como a chave HMAC é criada, distribuída e rotacionada, e qual o algoritmo e o cabeçalho da assinatura?
4. O que é a DLQ (tecnologia, quem consome, como um evento sai dela)?
5. Quais são o volume de clientes e de eventos e os serviços que hoje fazem POST manual vão migrar? Em que ordem?

Dois avisos sobre o que foi entregue:

- A imagem do diagrama de contêineres é um placeholder (`diagrams/entrega-webhooks-containers.svg`) que será renderizado na revisão manual. Sem Docker e sem a CLI do Structurizr nesta máquina, o DSL não foi validado. O código está dentro do bloco `<details>`, pronto para validação.
- O diagrama de sequência Mermaid também não foi validado nesta máquina, pois não há mermaid-cli disponível.
