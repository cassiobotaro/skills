Escrevi o design doc em `docs/design/dedup-de-eventos.md`. Ele ficou como DD-2026-001, em estado Rascunho, porque `docs/design/` só tinha o template. Segui as seções do template na ordem: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.

- **O que entrou:** tudo o que você disse: os 4% de duplicatas, as duas reclamações do financeiro, o serviço entre o ingestor e o Kafka, a chave no Redis por 24h e a meta de menos de 0,1%. O +5 ms de latência está como custo aceito na Proposta e como linha em Riscos. Também incluí um diagrama de sequência só com o fluxo que você descreveu.
- **Seção extra:** acrescentei "Alternativas consideradas" entre Proposta e Riscos, porque o template não tem lugar para as duas opções descartadas. Mantive o resto do esqueleto intacto. Se a arquitetura não aceitar a seção extra, dá para mover o conteúdo para dentro da Proposta.
- **Seções em aberto:** Plano de rollout só aponta para as perguntas, e a linha de Riscos tem a mitigação "a definir". Não inventei fases nem outros riscos. O campo Revisores também ficou vazio.
- **Alternativa "não fazer nada":** está registrada, mas sem a razão de ela ter perdido.
- **Skill `unslop`:** não rodei a passada de estilo, porque ela não está na lista de skills disponíveis. Revisei o texto à mão.

As perguntas estão no fim do documento, em 12 itens agrupados por tema. As que mais pesam são:
- Qual é o limite de latência da ingestão?
- Por que a janela é de 24h?
- Qual é o plano de rollout e o critério de rollback?
- De onde vem a chave idempotente?
- Quem revisa o documento?
