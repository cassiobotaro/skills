Salvei o documento em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`, no estado Rascunho. Não rodei nenhum passo de revisão além de reler o texto enquanto escrevia.

Ele segue as seções do template, na ordem: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas. Só usei o que você disse: os 4% de duplicatas, as duas reclamações do financeiro, o Redis com 24h, as duas alternativas descartadas, os +5 ms e a meta de 0,1%.

- **Seção extra:** o template não tem lugar para alternativas nem para o custo aceito. Criei "Alternativas consideradas" e "Custo aceito" como subseções de Proposta, sem mexer na ordem das seções do template. Se a arquitetura não aceitar isso, é só mover o conteúdo.
- **Seções quase vazias:** Plano de rollout está só com uma remissão às perguntas abertas, porque você não deu nada sobre fases ou rollback. Riscos tem uma linha só, a latência de +5 ms. Não escrevi outros riscos por conta própria; eles viraram perguntas.
- **Sem diagrama:** o fluxo exigiria detalhes que você não deu, como o formato da chave e a ordem entre gravar no Redis e publicar no Kafka.
- **Suposições minhas:**
  - Usei o número DD-2026-001, porque `docs/design/` só tinha o template.
  - A frase "não fazer nada" nas alternativas só deriva da motivação.
  - O campo Revisores ficou em branco.

As 10 perguntas abertas ficaram no final. As mais importantes para a arquitetura são:
- de onde vem a chave idempotente;
- por que 24h;
- o que acontece quando o Redis cai;
- como evitar perder ou duplicar um evento entre o Redis e o Kafka;
- o plano de rollout.

Nada foi commitado.
