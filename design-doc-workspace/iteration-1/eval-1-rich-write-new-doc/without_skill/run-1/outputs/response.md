Criei o design doc em `docs/design/exportacao-relatorios-background.md`.

Estruturei a partir do que você passou, cobrindo:

- **Resumo e contexto** — geração síncrona estourando o timeout de 30s, os 12% de falhas acima de 50 mil linhas e os tickets semanais de suporte.
- **Objetivos** — zerar timeouts e aguentar 100 mil linhas; com não-objetivos pra delimitar o escopo.
- **Solução** — API enfileira no RabbitMQ → worker gera CSV/XLSX em streaming → upload S3 → link assinado por e-mail, com diagrama de fluxo e descrição passo a passo.
- **Alternativas** — síncrono com timeout maior e BI externo, com o motivo de cada descarte (empurrar o problema / custo + exposição de PII).
- **Trade-off** — perda do download imediato e a unificação num caminho único só, com mitigações de UX.
- **Impacto em outros times** — Plataforma (fila compartilhada) e Segurança (link assinado com PII), com os pontos a alinhar com cada um.
- **Detalhes técnicos, segurança/privacidade, métricas de sucesso, plano de implementação, riscos/rollout e questões em aberto.**

Deixei alguns campos e decisões marcados como pendentes — vale você confirmar antes de circular o doc:

1. **Autor(es)/revisores** no cabeçalho (deixei `_(preencher)_`).
2. **Polling de UI na v1?** Entregar só o e-mail primeiro, ou já oferecer download na tela pros jobs que terminam rápido (aproximando a experiência atual das exportações pequenas)?
3. **Validade do link assinado** e se precisa de autenticação extra no download — fechar com Segurança.
4. **Retenção dos arquivos no S3** (quantos dias até o expurgo).
5. **Limite de concorrência / nº de workers** e isolamento da fila — fechar com Plataforma.
6. **Comportamento acima de 100 mil linhas** — bloquear, dividir em múltiplos arquivos, ou tratar depois?

Também não inventei stack/linguagem específica do worker nem nomes de serviços além do que você citou (RabbitMQ, S3). Se quiser, me diz a stack que eu detalho a parte de implementação.
