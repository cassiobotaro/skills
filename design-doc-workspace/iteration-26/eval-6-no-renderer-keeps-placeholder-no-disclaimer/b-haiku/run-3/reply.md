Escrevi o design doc em `docs/design/servico-webhooks-saida.md`. Ele tem o diagrama de arquitetura (C4 em Structurizr DSL, com o código-fonte dobrado em um bloco `<details>`) e o fluxo de entrega com retentativa (sequence diagram em Mermaid).

Algumas coisas ficaram em aberto porque você não as disse e eu não quis inventar:

1. O diagrama de contêineres ainda não está renderizado. Esta máquina não tem Docker nem a CLI do Structurizr, então a imagem é um placeholder marcado para o passo manual. Os blocos DSL e Mermaid também não foram validados aqui.
2. Esquema de retentativa: quais são os intervalos do backoff e o limite por tentativa, além das 24 horas?
3. Assinatura HMAC: qual algoritmo e cabeçalho usar, e como o segredo de cada cliente é guardado e rotacionado?
4. O que conta como resposta de sucesso (códigos HTTP específicos, ou qualquer resposta dentro de um tempo limite)? E o cliente recebe um identificador do evento para deduplicar?
5. A DLQ é um tópico Kafka, uma tabela no Postgres ou outra coisa, e quem trata as entregas que chegaram lá? Também preciso saber quem são os autores e revisores do documento.

As demais lacunas (metas mensuráveis, fora de escopo, custos além da latência, migração dos clientes que já recebem POST manual, retenção das tentativas) estão listadas na seção Questões em aberto do documento.
