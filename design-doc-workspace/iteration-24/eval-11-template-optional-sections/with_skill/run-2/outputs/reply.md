O doc está em `docs/design/servico-deduplicacao-eventos.md`, seguindo à risca a ordem do `docs/design/TEMPLATE.md`. O diagrama C4 fica como placeholder em `diagrams/arquitetura.svg`, com o DSL dobrado em `<details>`. Não renderizei a imagem (sem Docker): é para a passada manual.

**Seções do template**
- Preenchidas: Motivação, Proposta, Riscos, Métricas de sucesso (meta de 0,1% contra os 4% de hoje) e Perguntas abertas.
- Removidas, como o próprio template manda: Critérios de aceite (você não ligou o doc a uma história do backlog) e Estratégia de migração (não há dados existentes a migrar).
- Omitidas por serem opcionais e sem conteúdo seu: Histórias de usuário e Plano de rollout.

**Desvio do template, para você aceitar ou não:** acrescentei a seção "Alternativas consideradas" depois de Riscos, porque o template não tem onde registrar as alternativas que você descreveu. Incluí a alternativa "não fazer nada" a partir da dor que você contou, e nada além disso. Se o time de arquitetura não aceita seções extras, mova o conteúdo para a Proposta.

**O que ficou em branco por falta de informação:**
1. Revisores: quais áreas ou times devem revisar?
2. O número sequencial do documento (`DD-2026-<seq>`).
3. A chave idempotente: qual campo ou composição de campos a forma?
4. Se o Redis cair, o serviço descarta, deixa passar ou recusa o evento?
5. O rollout é gradual ou de uma vez, e existe rollback?
6. A seção Riscos só traz o risco que você citou (+5ms, ainda estimado, não medido). Há outros riscos e mitigações?

No diagrama não coloquei tecnologia nas caixas nem nas setas, porque você não a informou. Deixei só Redis e Kafka, que você citou.
