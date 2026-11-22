Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`, em português e com estado **Rascunho**. Não commitei nada.

**O que o doc contém**
- Glossário (PII, link assinado, streaming), visão geral e contexto, com os 12% de falha acima de 50 mil linhas e os tickets semanais do suporte.
- Objetivos: zerar os timeouts de exportação e suportar 100 mil linhas. Fora de escopo: manter o download imediato para exportações pequenas.
- Solução: API, fila RabbitMQ, worker e S3, com um diagrama de contêineres em Structurizr DSL e um diagrama de sequência em Mermaid.
- Trade-offs, com o custo de perder o download imediato em destaque.
- Alternativas: não fazer nada, timeout maior e BI externa, cada uma com o motivo de ter perdido.
- Preocupações transversais para Plataforma (fila compartilhada) e Segurança (link assinado com PII).

**O que ficou pendente**
- **Autores e revisores:** estão como "A preencher". Não assumi nomes.
- **Imagem do diagrama C4:** a referência `diagrams/architecture.svg` não existe ainda. Não rodei o renderizador, então precisa ser gerada a partir do DSL que está dobrado no doc.
- **Detalhes que você não me deu:** deixei como Perguntas em aberto, sem inventar resposta, e o diagrama os omite de propósito:
  - validade do link e retenção do arquivo no S3;
  - quem gera o link e quem envia o e-mail;
  - de onde o worker lê os dados;
  - se o bucket é novo;
  - o que acontece quando um job falha;
  - como a fila compartilhada isola as exportações;
  - rollout e rollback;
  - métricas e alertas.
- **Testes e plano de rollout:** não criei seções para eles, porque não havia conteúdo. Entraram só como perguntas.

Rodei as passadas de `technical-writing` e `unslop` no texto. Também tirei duas afirmações que eu tinha inferido e você não disse: "AWS" e um motivo ligado à memória do worker para o streaming.
