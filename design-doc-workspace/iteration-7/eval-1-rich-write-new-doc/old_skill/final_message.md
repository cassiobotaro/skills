O documento está pronto. Minha resposta final ao usuário, em português:

---

Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`, com o diagrama de contêineres renderizado em `docs/design/diagrams/exportacao-relatorios-containers.png`.

O que o documento cobre, a partir do que você me passou:

- **Problema e contexto**: geração na request da API, timeout de 30 s no gateway, ~12% de falha acima de 50 mil linhas, tickets semanais no suporte.
- **Objetivos mensuráveis**: zerar as falhas por timeout movendo a geração para fora da request, e suportar 100 mil linhas. **Fora de escopo**: manter caminho síncrono para exportações pequenas (a decisão de caminho único).
- **Design**: API publica o job no RabbitMQ existente → worker gera CSV/XLSX em streaming → upload para o S3 → e-mail com link assinado. A arquitetura está como diagrama C4 de contêineres (imagem renderizada, com a fonte em Structurizr DSL dobrada num bloco `<details>`) e o fluxo como diagrama de sequência Mermaid — apenas o caminho feliz, porque a política de falha do job ainda não foi definida.
- **Trade-offs explícitos**, incluindo o custo aceito (perda do download imediato) e os dois impactos externos: carga na fila compartilhada (Plataforma) e link assinado com PII (Segurança) — os dois times estão sugeridos como revisores no cabeçalho.
- **Alternativas**: timeout maior (só empurra o problema), BI externa (custo + expor dado de cliente) e "não fazer nada", com o porquê de cada descarte.

Sobre validação: o Structurizr DSL foi validado com a imagem Docker `structurizr/structurizr` (sem erros) e o PNG foi renderizado a partir dele. O diagrama Mermaid **não foi validado aqui** (não há Mermaid MCP nem mermaid-cli disponíveis) — GitHub/GitLab renderizam o bloco nativamente, e você pode conferir/editar em <https://mermaid.live>.

Ficaram pontos que só você pode responder — estão registrados na seção "Questões em aberto" do doc, e as respostas eu incorporo no corpo quando você tiver:

1. **Autores e revisores nominais** para o cabeçalho (deixei os times de Plataforma e Segurança sugeridos, sem nomes).
2. **De onde o worker lê os dados** — o mesmo banco da API? 100 mil linhas pesam nessa fonte?
3. **Contrato da API ao enfileirar** — status e id do job? Haverá endpoint de consulta de andamento, ou o e-mail é o único retorno?
4. **O que acontece quando o job falha** — retry, descarte, aviso ao usuário?
5. **Quem envia o e-mail** — já existe mecanismo de e-mail transacional no produto? E quais os requisitos de Segurança para o link assinado (expiração, escopo, revogação)?

Detalhe honesto do diagrama: os contêineres da API e do worker estão **sem tecnologia declarada** (você não citou a stack, e eu não invento) — quando me disser, atualizo o DSL e re-renderizo a imagem.
