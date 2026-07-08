O documento está pronto. Resposta final ao usuário, em português:

---

Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`. Como não havia outros design docs no repositório definindo um formato da casa, usei uma estrutura padrão: cabeçalho, glossário, visão geral, escopo e contexto, objetivos e fora de escopo, o design (visão da solução, arquitetura, fluxo, dados e sensibilidade), trade-offs, alternativas, preocupações transversais, testabilidade e questões em aberto.

O que você me passou cobriu o essencial, então escrevi direto:

- **Problema com números**: timeout de 30 s no gateway, ~12% de falha acima de 50 mil linhas, ticket semanal no suporte.
- **Objetivos mensuráveis**: zerar as falhas por timeout e suportar 100 mil linhas — e a seção de testabilidade deriva deles (teste de ponta a ponta com 100 mil linhas; taxa de falha por timeout como métrica, meta zero).
- **Trade-off central registrado com o custo na mesa**: a exportação pequena que hoje sai na hora vira assíncrona também — um caminho só, em troca do fim do download imediato.
- **Alternativas com o motivo da derrota**: timeout maior (só empurra o problema), BI externa (custo + exposição de dado de cliente) e não fazer nada (os 12% e os tickets continuam).
- **Times impactados** na seção transversal e como revisores no cabeçalho: Plataforma (carga na fila compartilhada) e Segurança (link assinado com PII).

Sobre os diagramas:

- A **arquitetura** está como Structurizr DSL dobrado num bloco `<details>`, **validado** com `structurizr/structurizr validate` (passou limpo). A imagem referenciada em `docs/design/diagrams/` ficou como placeholder: não há renderizador de PlantUML/Graphviz disponível aqui — na passada manual, `docker run --rm -v "$PWD":/usr/local/structurizr structurizr/structurizr local` sobe a UI em `localhost:8080` para exportar o PNG/SVG.
- O **fluxo** está em Mermaid (renderiza direto no GitHub/GitLab), mas **não foi validado aqui** — não há Mermaid CLI nem MCP disponível; se quiser conferir antes do commit, cole o bloco em <https://mermaid.live>. O diagrama mostra só o caminho feliz, de propósito: vocês ainda não definiram o comportamento em falha, e eu não quis inventar.

Ficaram **7 questões em aberto** registradas no doc — as respostas entram no corpo depois:

1. Quem assina como autor e quem revisa por Plataforma e Segurança?
2. O que a chamada de exportação responde (status/payload)? Vai existir consulta de andamento na interface, ou o e-mail é o único canal?
3. O que acontece quando a geração ou o upload falha no meio — reprocessa, descarta, avisa o usuário?
4. Qual o prazo de expiração do link assinado e a retenção dos arquivos no S3?
5. O e-mail sai por um serviço interno existente ou por um provedor a contratar?
6. Qual o volume esperado de jobs e os limites acordados com Plataforma na fila compartilhada?
7. Como comunicar aos usuários o fim do download imediato — e a mudança entra de uma vez ou por etapas?

Se me responder essas (mesmo que parcialmente), atualizo o documento — as de falha (3) e de segurança (4) são as que eu atacaria primeiro, porque mudam o design, não só o texto.
