Escrevi o documento em `docs/design/dd-2026-001-servico-de-deduplicacao-de-eventos.md`. Ele segue as seções do template, na ordem, e não rodei nenhuma verificação nele.

**Desvios do template, para você aceitar ou não:**
- Adicionei uma subseção "Alternativas consideradas" dentro de Proposta, com a deduplicação no consumidor, a idempotência nativa do Kafka e "não fazer nada". O template não tem lugar para isso, e o motivo de descartar cada uma faz parte da decisão. A subseção diz que não vem do template. Se a arquitetura recusar seções extras, apague-a.
- Também pus o trade-off dos +5 ms numa subseção "Trade-off aceito" dentro de Proposta.
- Incluí um diagrama de sequência em Mermaid com o fluxo de chave nova e chave repetida. Ele só usa o que você descreveu.

**Pontos que preenchi por conta própria:**
- O número **DD-2026-001**. Não havia outros docs na pasta, então assumi o primeiro do ano. Confirme.
- **Estado:** Rascunho. **Criado em** e **Última atualização:** 2026-11-23.

**Seções que ficaram sem substância:**
- **Riscos:** só entrou a latência de +5 ms, marcada como estimativa não medida.
- **Plano de rollout:** só registra "a definir", porque você não deu fases nem critérios.
- **Revisores:** vazio.
- **Perguntas abertas:** são 10, e as mais importantes são estas:
  - O que acontece quando o Redis cai.
  - Quem gera a chave idempotente.
  - O que acontece se a chave for gravada no Redis e a publicação no Kafka falhar.
  - Se a janela de 24h basta para o faturamento.
  - As fases e o gatilho de rollback.

Não inventei nenhuma resposta para essas perguntas. Não consegui verificar nada da arquitetura atual no repositório, porque ele só tem o template.
