Escrevi o rascunho do design doc do serviço de webhooks de saída em `docs/design/webhooks-saida.md`, com a arquitetura em Structurizr DSL e o fluxo de entrega com retry em Mermaid.

Algumas coisas ficaram em aberto, porque você não as descreveu e eu não quis inventá-las. As mais importantes para destravar a próxima versão:

1. Qual métrica mostra que os objetivos foram atingidos (por exemplo, percentual de eventos entregues dentro das 24 horas)?
2. Quais eventos de domínio entram na entrega, e como um evento se associa a cada cliente destinatário?
3. Qual é a política de backoff (intervalo inicial, fator, teto por tentativa, jitter) e o timeout de cada POST? O que conta como resposta de sucesso?
4. Onde fica a chave HMAC, quem a gera, como o cliente a recebe e como ela é rotacionada?
5. Quem são os autores e os revisores? Sugeri Segurança e Plataforma como revisores.

Também ficaram sem resposta: a tecnologia do serviço de entrega e da DLQ, o conteúdo do payload (se há dado pessoal), a forma de o cliente reconhecer reenvios duplicados, o que acontece com um evento na DLQ, e como os serviços atuais que fazem o POST por conta própria migram para o novo serviço. O restante está listado em "Questões em aberto" no próprio documento.

Observações sobre o que ficou fora deste ambiente:

- O diagrama de containers ficou como referência de imagem (`docs/design/diagrams/webhooks-saida-containers.svg`) ainda não renderizada. O DSL está dobrado logo abaixo, para a renderização na revisão manual. Não há Docker nem CLI do Structurizr aqui, então o DSL não foi validado.
- O bloco Mermaid do fluxo de retry também não foi validado localmente (não há Docker nem `mmdc`). Ele pode ser colado em qualquer Markdown que renderize Mermaid para conferir.
- Nenhum dos dois ganhou um aviso de validação dentro do documento, porque o aviso fica para a resposta, não para o texto do design.
