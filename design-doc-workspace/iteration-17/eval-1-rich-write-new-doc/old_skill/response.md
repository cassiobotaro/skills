Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`, com o diagrama de containers renderizado em `docs/design/diagrams/arquitetura-containers.svg`. O repositório não tinha nenhum design doc, então usei o catálogo padrão de seções (header, glossário, visão geral, contexto, objetivos, solução com arquitetura e fluxo, trade-offs, alternativas, preocupações transversais, testabilidade e questões em aberto) e a linguagem da conversa.

O que está no documento veio só do que você descreveu: o timeout de 30 s do gateway, os ~12% de falha acima de 50 mil linhas, os tickets semanais, o RabbitMQ já existente, o worker com geração em streaming, o S3 com link assinado por e-mail, as duas alternativas descartadas (síncrono com timeout maior; BI externa) mais "não fazer nada", o custo aceito (fim do download imediato, inclusive nas exportações pequenas) e os dois times impactados. Nos diagramas deixei em branco de propósito o que não foi estabelecido: a tecnologia da API e do worker, a fonte de dados que o worker lê e o mecanismo de envio de e-mail (aparece como um sistema externo genérico). O diagrama de sequência mostra só o caminho feliz.

Validação: o DSL do diagrama C4 passou no `structurizr/structurizr validate` (Docker) e o SVG foi gerado a partir dele (export para Mermaid, render com o `minlag/mermaid-cli`); o diagrama de sequência Mermaid também passou no `minlag/mermaid-cli`. Nada saiu da máquina.

As lacunas estão listadas na seção "Questões em aberto" do documento. As que mais mudam o desenho, e que valeria responder antes de mandar para revisão:

1. De onde o worker lê os dados do relatório? Se for o mesmo banco da API, qual o impacto de uma exportação de 100 mil linhas sobre ele? (com isso o diagrama ganha esse container)
2. O que acontece quando o job falha ou o e-mail não é entregue: há retentativa, e o usuário fica sabendo?
3. Qual a validade do link assinado e por quanto tempo o arquivo fica no S3? (é a pergunta que o time de Segurança vai fazer)
4. A exportação vai usar uma fila dedicada dentro do RabbitMQ compartilhado, e como se isola dos outros consumidores? (a pergunta do time de Plataforma)
5. O que fica explicitamente fora de escopo, e quem assina como autor e revisores?

Me passa as respostas que eu incorporo no corpo do documento e tiro da lista de questões em aberto. Para regerar o SVG depois de editar o DSL (que está dobrado num bloco `<details>` no próprio doc), salve o DSL como `workspace.dsl` e rode, na pasta dele:

```
docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes structurizr/structurizr export -workspace workspace.dsl -format mermaid -output diagrams
docker run --rm -u $(id -u):$(id -g) -v "$PWD/diagrams":/data minlag/mermaid-cli -i structurizr-Containers.mmd -o arquitetura-containers.svg
```
