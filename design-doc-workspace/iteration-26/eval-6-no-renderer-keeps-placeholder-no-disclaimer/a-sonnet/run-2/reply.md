Escrevi o design doc em `docs/design/webhooks-de-saida.md`, em português, com o que você descreveu: problema, objetivos, arquitetura, fluxo de entrega com retry, trade-offs, alternativas (SaaS descartado e "não fazer nada") e perguntas em aberto.

Sobre os diagramas:
- A arquitetura está em Structurizr DSL, dobrada num bloco `<details>`. A referência de imagem `diagrams/arquitetura.svg` ficou como placeholder, com uma nota de "renderizar na passada manual", porque aqui não há Docker nem CLI do Structurizr. A imagem ainda precisa ser gerada.
- O fluxo de entrega com retry é um bloco Mermaid, que renderiza direto no GitHub e no GitLab.
- O DSL e o Mermaid não foram executados por nenhum validador nesta máquina. Para validar o DSL: `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl`. Para o Mermaid: `docker run --rm -u "$(id -u):$(id -g)" -v "$DIR":/data minlag/mermaid-cli -i d.mmd -o d.svg`.
- Deixei sem tecnologia as caixas que você não nomeou (serviço de entrega, DLQ, Kafka como fila), em vez de adivinhar.

Perguntas para fechar o documento (estão também em "Perguntas em aberto"):
1. Quem são os autores e quais áreas ou equipes devem revisar (segurança, donos dos serviços que hoje fazem o POST)?
2. Qual é a curva do backoff (intervalo inicial, fator, teto)?
3. O que conta como sucesso: qualquer 2xx? Uma resposta 4xx do cliente é reenviada ou é falha definitiva? O diagrama só mostra a indisponibilidade do endpoint porque foi o único caso que você descreveu.
4. Como o cliente obtém e rotaciona a chave do HMAC?
5. Quem consome a DLQ e o que faz com os eventos?
6. Como a equipe consulta as tentativas registradas?
7. A migração dos serviços de domínio é de uma vez ou em etapas, e há rollback?
8. Qual tecnologia sustenta a DLQ e o agendamento dos reenvios?
