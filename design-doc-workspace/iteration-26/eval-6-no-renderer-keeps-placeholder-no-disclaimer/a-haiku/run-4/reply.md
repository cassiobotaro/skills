Escrevi o rascunho do design doc em docs/design/webhooks-saida.md. Ele traz a visão da solução, o diagrama de contêineres (C4 em Structurizr DSL), o fluxo de entrega com retry (diagrama de sequência em Mermaid), os trade-offs, as alternativas, as preocupações transversais e as questões em aberto.

Pontos que ficaram em aberto e preciso que vocês confirmem:

1. Autores e revisores. Sugiro Segurança (assinatura HMAC e dados que saem da borda) e Plataforma (operação sobre Kafka e Postgres).
2. Critério de sucesso de um POST (quais códigos HTTP contam) e tempo limite por chamada.
3. Backoff: intervalo inicial, teto e jitter. A janela de 24 horas começa no primeiro envio?
4. HMAC: algoritmo, cabeçalho e ciclo de vida da chave por cliente.
5. Payload: formato, e se ele tem dado pessoal.
6. DLQ: onde fica (tópico, tabela ou outra coisa) e quem trata os eventos nela.
7. Garantias: o cliente pode receber o mesmo evento duas vezes? Há ordem por cliente?
8. Volume (eventos por dia, número de clientes) e a métrica que prova a meta de nenhum evento perdido.
9. Quem consulta as tentativas e por qual interface.
10. Quais serviços fazem POST hoje e em que ordem migram.
11. Tecnologia do serviço de entrega.

Sobre a renderização e a validação: nesta sessão não houve renderizador. O diagrama de contêineres ficou como referência de imagem (diagrams/webhooks-saida-containers.svg) a ser renderizada na passagem manual, com o DSL fonte dobrado num bloco details logo abaixo. O DSL não foi validado e o bloco Mermaid não foi validado. Para validar, rodem os comandos de validação do Structurizr e do mermaid-cli na máquina de vocês.

Observação: o ambiente desta execução tem o binário docker e o mmdc no PATH, apesar de a descrição da tarefa dizer que não há Docker. Não os executei, para não puxar imagens sem pedido. Se a máquina de vocês tiver o daemon Docker ativo, a validação pode ser feita de imediato.
