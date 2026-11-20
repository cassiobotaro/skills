Escrevi o design doc em `docs/design/webhooks-de-saida.md`, com o diagrama de arquitetura (DSL do Structurizr dobrado em `<details>`) e o fluxo de entrega com retry (Mermaid).

**Diagramas não validados.** Sem Docker, sem a CLI do Structurizr e sem mermaid-cli aqui, nada foi validado nem renderizado. A imagem `diagrams/architecture.svg` é um placeholder no doc; renderize na passagem manual. Para depois:

- Validar o DSL: `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl`
- Exportar SVG: use a imagem `structurizr/structurizr:<versão>-playwright` com `export -format svg`.
- Validar o Mermaid: `docker run --rm -u "$(id -u):$(id -g)" -v "$DIR":/data minlag/mermaid-cli -i d.mmd -o d.svg`. O GitHub e o GitLab também renderizam o bloco direto.

**O que deixei de fora ou em aberto, para não inventar.** Estas perguntas estão na seção "Questões em aberto":

1. Quem são os autores e os revisores (segurança, plataforma, times que publicam eventos)? O cabeçalho ficou sem essas linhas.
2. Quais são os intervalos do backoff e o que conta como falha (só endpoint fora do ar, ou também respostas de erro e timeout)?
3. Como o reenvio é agendado entre as tentativas, e qual é o mecanismo da DLQ? Deixei a tecnologia da DLQ em branco no diagrama.
4. Onde ficam e como são rotacionados os segredos HMAC? Como os clientes cadastram o endpoint?
5. Como o objetivo "nenhum evento perdido" será medido?
6. Há algo explicitamente fora de escopo? Não incluí a seção, porque você não citou nada.
7. Como as tentativas ficam visíveis (consulta, painel, alerta) e como os serviços atuais migram?

Dois pontos sobre o diagrama de arquitetura:

- Incluí "Serviços de domínio" publicando no Kafka como contexto, a partir do que você disse sobre os eventos que já temos.
- Usei "HTTP POST" na seta para o cliente, sem HTTPS, porque você não especificou o protocolo.
