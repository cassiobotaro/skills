Escrevi o design doc em `docs/design/servico-webhooks-saida.md`. Ele traz o glossário, o contexto, os objetivos, a arquitetura (C4 com o DSL dobrado), o fluxo de entrega com retry (sequence diagram em Mermaid), os trade-offs, as alternativas (incluindo "fazer nada" e o SaaS), as preocupações transversais e as perguntas em aberto.

Sobre o diagrama de arquitetura: a imagem ficou como referência `diagrams/architecture.svg` marcada para renderizar no passo manual, com o DSL logo abaixo, dentro de um bloco `<details>`. Você pediu que a máquina não tivesse renderizador, então não gerei a imagem.

Sobre a validação: o DSL passou no `structurizr validate` (exit 0) e o diagrama de sequência renderizou com o `mmdc` local. Observação: a sua mensagem diz que não há Docker nesta máquina, mas o daemon respondeu e há imagens do Structurizr e do mermaid-cli em cache. Se quiser a imagem PNG/SVG, a versão `-playwright` que já está em cache serve para exportar; eu não gerei sem pedido explícito.

Perguntas que precisam de resposta antes de fechar o documento:

1. Como medir "nenhum evento perdido"? Por exemplo, o percentual de eventos entregues dentro das 24 horas.
2. Quais eventos de domínio entram no serviço, e o que fica fora do escopo?
3. Quais são a base, o fator e o teto do backoff exponencial?
4. Qual resposta do cliente conta como entrega confirmada?
5. A entrega precisa preservar a ordem dos eventos, por cliente ou por agregado?
6. Se a confirmação se perde depois de o cliente receber o evento, ele recebe o mesmo evento de novo? Precisa de um identificador para deduplicar?
7. Quem gera, guarda e rotaciona a chave HMAC de cada cliente? Qual é o cabeçalho da assinatura e o que ela cobre?
8. A DLQ é um tópico do Kafka ou um armazenamento próprio? Quem reprocessa os eventos que caem nela?
9. O conteúdo do evento é gravado no Postgres? Por quanto tempo as tentativas ficam guardadas? Qual é o volume de eventos e de clientes?
10. Qual é a tecnologia do serviço de entrega? Deixei esse campo vazio no diagrama.
11. Quantos serviços fazem o POST por conta própria hoje, e como cada um migra? O serviço entra em produção de uma vez ou por etapas, e existe plano de volta?
12. Quem são os autores e os revisores? Sugeri Segurança, pelas chaves HMAC, e os times donos dos serviços que hoje fazem o POST.
