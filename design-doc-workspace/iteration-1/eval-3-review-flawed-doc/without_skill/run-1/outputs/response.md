Revisei o `docs/design/fanout-de-notificacoes.md` e já apliquei direto tudo que não dependia de você. O que precisa de informação sua eu deixei marcado no próprio doc com `TODO` e listei aqui embaixo.

## O que eu corrigi/melhorei direto

1. **Bug no diagrama**: faltava a DLQ do canal in-app — push e e-mail tinham DLQ, in-app não, mesmo o texto dizendo "DLQ por canal". Adicionei `WI --> DLQI[DLQ in-app]`.
2. **"Fora de escopo" estava trocado**: "o sistema não deve ser lento" e "não deve perder notificações" não são itens fora de escopo, são requisitos. Movi para Objetivos e preenchi a seção de Fora de escopo com itens que de fato são não-objetivos (providers, schema, opt-out, templates/i18n).
3. **Objetivos vagos** ("melhorar performance", "ser escalável", "garantir SLA") reescritos como metas mensuráveis — mas com números como placeholder, porque sem dados eles não são verificáveis (ver perguntas).
4. **Frase sem fundamento na Solução** ("mais escalável e robusta, mais fácil de manter") substituída pela descrição concreta do fluxo, passo a passo.
5. **Estrutura**: adicionei as seções que faltavam para um design doc revisável — Contexto/problema, Garantias e pontos de atenção (idempotência, TPS, ordenação, DLQ), Alternativas consideradas, Observabilidade, Riscos e mitigações. O Plano foi detalhado para uma migração segura (publicar em paralelo, garantir idempotência antes de ligar os dois fluxos, migrar canal a canal, rollback por etapa).

Observação: tentei validar/renderizar o diagrama Mermaid pelo servidor MCP, mas ele está retornando erro de transporte agora. A mudança é só um nó + uma aresta seguindo exatamente o mesmo padrão das linhas existentes, então a sintaxe está ok; só não consegui gerar o preview.

## Preciso de você (estão como TODO no doc)

**Números (sem eles os objetivos ficam não-mensuráveis):**
1. Volume atual: notificações/dia e pico por minuto?
2. Latência atual de entrega (p50/p95/p99) entre criação e envio?
3. Metas: qual latência p95 alvo, qual pico/min a suportar, e qual o SLA exato (ex. 99% em até X)?
4. Quais dores/incidentes motivaram a mudança (atrasos em pico, retries manuais, perdas)?

**Decisões de design:**
5. Idempotência: como evitar envio duplicado? Dedup por `notification_id`? (relevante porque cron antigo + novo fluxo vão coexistir na migração)
6. Controle de TPS por provider: token bucket no worker, prefetch limitado, ou limitador centralizado?
7. Existe algum caso que dependa de ordem (ex. "lida" depois de "recebida")? O fanout não garante ordem global.
8. DLQ: reprocessamento manual, automático com backoff, ou ambos? Política de retenção?
9. Alternativas consideradas e por que descartadas (ex. paralelizar o cron com worker pool; broker escolhido — RabbitMQ/SQS/Kafka — e por quê)?
10. Observabilidade: onde ficam os dashboards/alertas (Grafana, Datadog, outro)?
11. Rollback: o que dispara reverter um canal para o cron durante a migração?

Me passa esses pontos que eu fecho o doc.
