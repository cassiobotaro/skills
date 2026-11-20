Escrevi o design doc em `docs/design/webhooks-saida.md`, em português, com o diagrama de arquitetura (C4 em Structurizr DSL) e o fluxo de entrega com retry (Mermaid).

Sobre o que não consegui fazer: sem Docker e sem a CLI do Structurizr, o diagrama de arquitetura não foi renderizado. O doc tem a referência `diagrams/architecture.svg` como placeholder e o DSL dobrado em um bloco `<details>` logo abaixo. Gere a imagem na passagem manual de revisão. O fluxo em Mermaid renderiza direto no GitHub/GitLab e também não foi validado localmente. Para validar depois: `docker run --rm -u "$(id -u):$(id -g)" -v "$DIR":/data minlag/mermaid-cli -i d.mmd -o d.svg`.

Escrevi só o que você contou. Deixei em branco o que não foi dito, e isso virou perguntas em aberto no fim do doc. Preciso de você para fechar:

1. Quem são os autores e quais áreas devem revisar (segurança, plataforma, as equipes dos serviços que hoje fazem o POST)? O cabeçalho está com "A definir".
2. Qual a meta numérica de sucesso (por exemplo, % de eventos entregues dentro das 24h)?
3. Quais são os parâmetros do backoff (intervalo inicial, fator, teto) e quais respostas do cliente contam como sucesso ou como falha com novo envio?
4. De onde vêm o endpoint e o segredo HMAC de cada cliente? Em que tecnologia roda a DLQ e quem age sobre o que cai nela?
5. Em que casos a entrega deixa de ser imediata e qual atraso é aceitável? Há plano de migração dos serviços atuais?

Por ora não atribuí tecnologia à DLQ nem ao serviço de entrega nos diagramas, pelo mesmo motivo.
