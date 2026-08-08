Escrevi o documento em `docs/design/exportacao-de-relatorios-em-background.md`. Como não havia design doc anterior no repositório, não existe um template da casa para seguir — usei uma estrutura padrão, escolhendo só as seções que este problema pede. Se vocês tiverem um template (wiki, drive), me passa que eu reencaixo o conteúdo nele.

O que o doc registra, tudo a partir do que você contou: o problema (geração dentro da request, corte de 30s no gateway, ~12% de falha acima de 50 mil linhas, ticket de suporte toda semana), os objetivos (zerar timeout e aguentar 100 mil linhas), a solução (API enfileira no RabbitMQ → worker gera CSV/XLSX em streaming → S3 → link assinado por e-mail), o custo aceito (perder o download imediato, inclusive nas exportações pequenas, em troca de um caminho só), as alternativas (síncrono com timeout maior, BI externa e "não fazer nada") e os impactos em Plataforma (fila compartilhada) e Segurança (link assinado com PII).

Dois diagramas:

- **Arquitetura (C4 de contêineres)** — escrita em Structurizr DSL, dobrada num `<details>` sob a referência de imagem `diagrams/arquitetura.svg`. Aqui não tem Docker nem Structurizr CLI, então a imagem ficou como marcador: dá pra gerar na passagem manual com o `export` do Structurizr a partir do DSL que está no doc.
- **Fluxo da exportação (sequência)** — bloco ```mermaid, que o GitHub/GitLab renderiza direto no Markdown. Não consegui validar por aqui (sem MCP de Mermaid e sem mermaid-cli); se quiser conferir antes, é colar em <https://mermaid.live>.

Duas coisas eu deliberadamente **não** preenchi, para não virarem decisão por acidente no diagrama: a tecnologia da API e do worker, e de onde o worker lê os dados do relatório. Deixei como pergunta em aberto.

Para fechar o rascunho, preciso de você:

1. **Autores e revisores** — o cabeçalho está com `(a preencher)`. Sugeri Plataforma e Segurança como áreas revisoras; quem são as pessoas?
2. **Fora de escopo** — o que alguém poderia razoavelmente esperar desta entrega e que vocês já decidiram deixar de fora? Hoje essa lista está vazia.
3. **Falha e retentativa** — o diagrama mostra só o caminho feliz. O que acontece quando o worker morre no meio da geração, ou quando o envio ao S3 ou o e-mail falha? O usuário fica sabendo?
4. **Validade do link e retenção no S3** — é o primeiro número que o time de segurança vai pedir.
5. **Como vocês vão verificar os objetivos** — qual métrica mostra "zero timeouts" em produção, e como testar as 100 mil linhas antes de subir? Com isso eu escrevo a seção de testabilidade e observabilidade, que hoje não existe porque não tinha substância para ela.

Também não escrevi plano de implantação — se a troca do endpoint síncrono pelo assíncrono quebra algum consumidor e precisa de convivência entre os dois, me diz que eu acrescento a seção.
