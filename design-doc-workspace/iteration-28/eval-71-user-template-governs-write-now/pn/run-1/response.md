Escrevi o design doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`, no estado Rascunho. Não rodei nenhuma checagem além de escrever o arquivo.

**Template**
- O doc tem todas as seções de `TEMPLATE.md`, na mesma ordem.
- Fiz um desvio: o template não tem seção de alternativas, então coloquei **Alternativas consideradas** e **Trade-off aceito** como subseções da Proposta. As duas alternativas descartadas estão numa tabela com o motivo de cada uma. Se a arquitetura preferir outro lugar, é só mover.

**O que ficou no doc**
- Só o que você disse: os 4% de duplicatas, o financeiro, o serviço entre o ingestor e o Kafka, as chaves no Redis por 24h, as duas alternativas, os +5 ms e a meta abaixo de 0,1%.
- Não fiz diagrama. O fluxo depende da ordem entre gravar no Redis e publicar no Kafka, que você não definiu, e eu não quis inventar essa ordem.
- Em Riscos, só entraram a latência e a janela de 24h. A janela é consequência direta do desenho: um reenvio depois de 24h não é detectado.

**Seções em aberto**
- **Plano de rollout:** não tive substância, então a seção só diz que está em aberto e aponta para as perguntas. Escolhi isso em vez de inventar fases.
- **Revisores:** deixei em branco.
- **Número do documento:** usei `DD-2026-001` porque não há outros docs no repositório. Confirme se esse número está livre.

**Perguntas abertas (as 8 estão no fim do doc)**
1. O que acontece se o Redis ou o serviço cair: deixa passar duplicata ou bloqueia a ingestão?
2. Quem gera a chave idempotente e em que formato?
3. O serviço grava a chave antes ou depois de publicar no Kafka? Se gravar antes e a publicação falhar, o retry do produtor seria descartado e o evento se perderia.
4. Quais são as fases do rollout e os critérios de avanço e de rollback?
5. Qual o volume diário de eventos, para dimensionar o Redis?
6. Existe um custo estimado das duplicatas para o financeiro, para comparar com o custo do serviço? A alternativa "não fazer nada" não foi discutida.
7. O que está fora de escopo?
8. Quem são os revisores e o número do doc está certo?

As perguntas 1, 3 e 4 são as que o time de arquitetura provavelmente vai cobrar primeiro.
