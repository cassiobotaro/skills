Escrevi o documento em `docs/design/dedup-de-eventos.md`, seguindo as seções do `TEMPLATE.md` na mesma ordem. Não rodei a skill `unslop` nem renderizei o diagrama, e o texto não passou por revisão de estilo.

- **Alternativas e trade-off:** o template não tem seção para elas. Como você exigiu o formato à risca, não criei seção de topo. Elas entraram como subseções dentro de Proposta ("Alternativas consideradas" e "Trade-off aceito"). Se o time de arquitetura preferir outro lugar, é só mover.
- **Meta:** a meta de duplicatas abaixo de 0,1% (hoje 4%) ficou em Métricas de sucesso.
- **Diagrama:** há um diagrama de containers (Ingestor, serviço de dedup, Redis, Kafka) com o código Structurizr dobrado embaixo. A imagem `diagrams/dedup-de-eventos.svg` ainda não existe, então a referência é um placeholder. Não coloquei tecnologia nem protocolo nas setas, porque você não os informou.
- **Riscos e Rollout:** só o risco de latência (+5ms) entrou em Riscos, porque foi o único que você levantou. Não inventei outros riscos nem fases de rollout. Essas duas seções apontam para as perguntas abertas.
- **Cabeçalho:** o estado é Rascunho, o autor é Rafael Nunes, a data é 2026-11-23 e os revisores estão em branco. Numerei como DD-2026-001 porque não há outros docs no repositório.

Deixei 11 perguntas no final. As mais importantes:
- Quem gera a chave idempotente, e o retry sempre carrega a mesma chave?
- O que o ingestor faz se o serviço ou o Redis cair: rejeita ou encaminha sem deduplicar?
- O que fazer se o serviço gravar a chave no Redis e falhar antes de publicar no Kafka? Nesse caso o retry do produtor seria descartado e o evento se perderia.
- Um reenvio depois de 24h passa como evento novo. O time aceita isso?
- Quais são as fases e os critérios de rollout e de rollback?
- Qual é o limite de latência aceitável, além da estimativa de 5ms?
- Quem revisa o documento?
