Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`, com o diagrama de containers renderizado em `docs/design/diagrams/exportacao-de-relatorios-containers.svg`.

O que o documento cobre, tudo a partir do que você trouxe: o problema (geração na request, timeout de 30 s no gateway, ~12% de falha acima de 50 mil linhas, ticket semanal do suporte), os dois objetivos (zerar timeouts, aguentar 100 mil linhas), a solução (API enfileira no RabbitMQ, worker gera CSV/XLSX em streaming e sobe pro S3, link assinado por e-mail), o diagrama de containers em Structurizr DSL (imagem no topo, fonte dobrada num bloco `<details>`) e o fluxo de exportação em Mermaid, os trade-offs (caminho único assíncrono em troca do download imediato, carga na fila compartilhada, link com PII), as alternativas (não fazer nada, síncrono com timeout maior, BI externa) e as preocupações dos times de plataforma e segurança.

Deixei em branco, de propósito, o que a conversa não estabeleceu. Vale a pena responder antes de mandar para revisão:

1. **Autores e revisores**: quem assina e quem revisa por plataforma e por segurança? O cabeçalho está com "A definir".
2. **Fonte dos dados**: de onde o worker lê o relatório (o mesmo banco da API? uma réplica?). Isso não está no diagrama, e uma leitura de 100 mil linhas nessa fonte é um impacto que o doc hoje só aponta como pergunta.
3. **Tecnologia da API e do worker**: os dois containers estão sem tecnologia no DSL; me diz a stack e eu preencho.
4. **Resposta da API e acompanhamento**: o que a API devolve ao enfileirar, e como o usuário sabe que a exportação está em andamento enquanto o e-mail não chega?
5. **Falhas**: o diagrama de sequência mostra só o caminho feliz. O que acontece quando o job falha ou o e-mail não é entregue (retentativa? aviso ao usuário)?
6. **Quem manda o e-mail**: desenhei o worker disparando o envio ao terminar, por um serviço de e-mail que não foi nomeado. Se for outro componente, ajusto.

Também não inventei o que fica fora de escopo nem o plano de entrega (de uma vez ou em etapas); os dois estão como perguntas na seção Questões em aberto, junto com as de segurança (validade do link, retenção no bucket, e-mail como canal) e de plataforma (fila dedicada ou compartilhada, volume de jobs, dimensionamento do worker).

Sobre validação: o DSL foi validado com `structurizr/structurizr validate` (exit 0) e exportado para PlantUML, renderizado em SVG com a imagem `plantuml/plantuml`; o diagrama Mermaid foi validado com a imagem `minlag/mermaid-cli` (exit 0). O layout automático do diagrama de containers ficou um pouco apertado nos rótulos das setas; se quiser ajustar à mão, o `structurizr/structurizr local` abre a UI de preview e salva o layout.

---

Arquivos escritos:
- `/home/cassiobotaro/Projetos/skills/design-doc-workspace/iteration-17/eval-1-rich-write-new-doc/with_skill/outputs/docs/design/exportacao-de-relatorios-em-background.md`
- `/home/cassiobotaro/Projetos/skills/design-doc-workspace/iteration-17/eval-1-rich-write-new-doc/with_skill/outputs/docs/design/diagrams/exportacao-de-relatorios-containers.svg`

Arquivos de referência das skills lidos:
- design-doc: `SKILL.md`, `references/sections.md`, `references/diagrams.md`
- structurizr: `SKILL.md`, `references/dsl-reference.md`, `references/modeling-patterns.md`
- mermaid-sequence: `SKILL.md`, `references/syntax.md`

Validadores executados:
- `structurizr/structurizr validate -workspace workspace.dsl` (Docker): exit 0, sem erros. Depois `export -format plantuml` (exit 0) e `plantuml/plantuml -tsvg` (exit 0) para gerar o SVG.
- `minlag/mermaid-cli -i d.mmd -o d.svg` (Docker): exit 0, "Generating single mermaid chart", SVG gerado.
