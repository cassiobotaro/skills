Pronto! Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`.

Seu brief já trazia o essencial (problema, números, solução, alternativas descartadas, trade-off aceito e times impactados), então escrevi direto em vez de ficar te interrogando. Estrutura do doc:

- **Header + glossário** (AMQP, S3, TTL, PII, signed URL etc.).
- **Overview / Escopo e contexto**: o timeout de 30s do gateway, os ~12% de falhas acima de 50k linhas e os tickets semanais.
- **Objetivos mensuráveis**: zerar timeouts, suportar 100k linhas, ter um caminho único de exportação.
- **A solução**: visão geral + diagrama de container (C4) + diagrama de sequência do fluxo, cada um com texto explicando os componentes e o porquê.
- **Trade-offs explícitos** (✓/✗), com o custo aceito em destaque: perda do download imediato, inclusive para exportação pequena.
- **Alternativas** numa tabela, incluindo "não fazer nada", além das duas que vocês descartaram (síncrono com timeout maior; BI externa).
- **Cross-cutting concerns**: Segurança (link assinado com PII) e Plataforma (fila compartilhada), mais compatibilidade do contrato da API. Sugeri os dois times como revisores no header.
- **Testabilidade/observabilidade**, **plano de implantação** em 4 etapas atrás de flag, e **questões em aberto**.

Sobre os diagramas: o de container (C4) eu modelei e validei no Structurizr antes de embutir. O de sequência está em Mermaid inline, mas o servidor de validação de Mermaid estava fora do ar, então esse não foi validado por máquina (deixei a nota no doc); modelei a mesma sequência como dynamic view no Structurizr pra conferir a ordem dos passos.

Não inventei nada que você não tenha dito. O que ficou em aberto eu marquei como "a definir" / "questões em aberto", em vez de chutar. Vale você completar/confirmar:

1. **Autores e revisores nomeados** do doc (deixei Plataforma e Segurança como sugestão).
2. **TTL da URL assinada** e **política de retenção/expiração** dos arquivos com PII no S3.
3. **Qual serviço/infra de e-mail** será usado pra entregar o link.
4. Vai existir um **endpoint de status/rastreio do job** (usando o ID que a API devolve no 202), ou o e-mail é o único feedback?
5. **Quem consome a API de exportação hoje** e como será a transição do contrato síncrono → assíncrono.
6. **Retentativa/DLQ** para jobs que falham (alinhar com Plataforma).
7. Na etapa 3 do rollout, **a partir de quantas linhas** a exportação vira assíncrona antes de unificar tudo.

Se quiser, me passa essas respostas que eu já incorporo no doc e atualizo a data de "Última atualização".
