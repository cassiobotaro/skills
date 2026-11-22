Passei as duas revisões de prosa (`technical-writing` e `unslop`) no documento e não achei mais nada para ajustar. Só troquei um passivo sem agente em Riscos.

O doc está em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`, no estado Rascunho. Ele usa as seis seções do template, na ordem, e o cabeçalho com você como autor e as datas de hoje (2026-11-22). Não rodei nenhum comando do projeto, e o doc não tem diagrama.

**Onde fugi do template à risca**
- **Seção de Proposta:** coloquei "Trade-offs" e "Alternativas consideradas" como subseções (`###`) dentro dela. Você deu essa substância e o template não tem onde guardá-la. Assim o esqueleto de seções fica intacto. Se a arquitetura preferir sem as subseções, é só remover, mas o doc perde os custos aceitos e as alternativas descartadas.
- **Alternativas:** incluí "não fazer nada", com o motivo vindo só da dor que você descreveu (4% de duplicatas e duas reclamações do financeiro).
- **Número do documento:** usei `DD-2026-001` porque só existe o TEMPLATE em `docs/design/`. Ajuste se a numeração real for outra.

**Pontos que ficaram sem resposta**
- **Revisores:** o campo está vazio.
- **Plano de rollout:** você não deu fases nem critério de rollback. A seção só aponta para as perguntas abertas, sem fases inventadas.
- **Riscos:** só o +5 ms está estabelecido, e continua como estimativa não medida. Falha do serviço ou do Redis e reenvio depois das 24h entraram como risco com mitigação indefinida.

**Perguntas abertas**

São 9 no final do documento. As mais importantes:
- Quem gera a chave idempotente, e ela já existe em todos os eventos?
- Qual é a ordem entre gravar a chave no Redis e publicar no Kafka? Se o serviço gravar a chave e falhar antes de publicar, o retry do produtor é descartado e o evento se perde.
- O que acontece com a ingestão se o serviço ou o Redis cair?
- A janela de 24h cobre o tempo em que os produtores reenviam?
