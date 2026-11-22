Salvei o doc em `docs/design/deduplicacao-de-eventos.md`, com as seis seções do template, na ordem e com os títulos originais. Não commitei nada.

**Desvio do template**
- O template não tem lugar para alternativas nem para o trade-off aceito, e você deu os dois. Coloquei os dois como subseções de Proposta (`### Alternativas consideradas` e `### Trade-off aceito`), sem criar seção de primeiro nível. "Não fazer nada" entrou como alternativa, com a dor que você descreveu. Se o time de arquitetura só aceita as seis seções sem subseção, é só mover o conteúdo.
- Incluí um diagrama de sequência em Mermaid, seguido de texto. Não fiz diagrama C4: ele pediria tecnologia em cada caixa e seta que você não deu.

**Escrito só com o que você disse**
- Motivação: 4% de duplicatas em outubro de 2026 e as duas reclamações do financeiro.
- Proposta: o serviço entre o ingestor e o Kafka, as chaves no Redis por 24h e o descarte de repetidos.
- Alternativas e métrica: as duas alternativas que você descartou, com os motivos, e a meta de duplicatas abaixo de 0,1%.
- Trade-off: o salto a mais no caminho crítico, com a estimativa de +5 ms.

**Em aberto**
- O cabeçalho ficou com `DD-2026-<seq>` e sem revisores, porque não sei o número sequencial nem quem revisa.
- Plano de rollout e Riscos ficaram quase vazios: você não deu fases, critérios de avanço, rollback nem mitigações, e não inventei nenhum.
- Todas as lacunas viraram perguntas no final, agrupadas por seção. As principais:
  - o que o serviço faz com o Redis fora do ar;
  - se a chave é gravada antes ou depois da confirmação do Kafka;
  - quem gera a chave idempotente;
  - o que acontece com reenvios depois de 24h.

O `unslop` tirou do texto três afirmações que você não fez: uma consequência para os consumidores, uma mitigação de latência e um motivo a mais no "não fazer nada".
