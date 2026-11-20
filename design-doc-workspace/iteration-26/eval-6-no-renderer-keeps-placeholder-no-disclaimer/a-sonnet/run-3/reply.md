Escrevi o design doc em `docs/design/webhooks-de-saida.md`, com o diagrama de arquitetura (Structurizr DSL dobrado em `<details>`) e o fluxo de entrega com retry (Mermaid).

Dois pontos sobre o ambiente:
- Sem Docker nem CLI do Structurizr, não renderizei a imagem. O doc tem a referência `diagrams/Containers.svg` como placeholder, com uma nota para renderizar na passada manual. O arquivo ainda não existe.
- O Mermaid não foi validado aqui. Para validar: `docker run --rm -u "$(id -u):$(id -g)" -v "$DIR":/data minlag/mermaid-cli -i d.mmd -o d.svg`. O GitHub e o GitLab também renderizam o bloco direto.

Só escrevi o que você disse. Deixei de fora, de propósito, tecnologia da DLQ, critério de sucesso, intervalos do backoff e protocolo nas setas. Preciso de resposta para estes pontos, que estão em "Questões em aberto":
1. Quem são os autores e quais áreas devem revisar?
2. Como medir "nenhum evento perdido" e "visibilidade de cada tentativa"? Existe uma métrica ou uma tela de consulta?
3. Qual resposta do cliente conta como sucesso, e quais são os intervalos do backoff?
4. Qual é a tecnologia da DLQ, quem trata o que cai nela, e onde fica guardado o agendamento dos reenvios?
5. Como o endpoint e o segredo HMAC de cada cliente são cadastrados?
6. O que fica fora do escopo, e qual é o plano de migração dos serviços atuais?
7. Em quais casos a entrega deixa de ser imediata, e qual atraso é aceitável?
