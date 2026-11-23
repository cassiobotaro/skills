Salvei o documento em `docs/design/dd-2026-001-deduplicacao-de-eventos.md`. Não rodei `scripts/validate.py` nem fiz commit.

Segui as seções do `TEMPLATE.md` na ordem original, com cabeçalho e estado "Rascunho". Escrevi só o que você disse. Esta é a divisão por seção:

- **Motivação e Proposta:** a Motivação traz os 4% de duplicatas e as duas reclamações do financeiro. A Proposta traz o fluxo ingestor → serviço → Kafka, com a chave guardada no Redis por 24h. Registrei também o custo aceito de +5 ms e que reenvios depois de 24h não são reconhecidos.
- **Riscos:** latência (+5 ms), o Redis como nova dependência e as duplicatas fora da janela de 24h.
- **Métricas de sucesso:** duplicatas abaixo de 0,1% e a latência medida contra a estimativa de 5 ms.
- **Plano de rollout:** não me deu base para inventar fases, então a seção só diz que ainda não foram definidas e aponta para as perguntas abertas.
- **Perguntas abertas:** são oito, no final do documento. As principais são quem gera a chave idempotente, o que acontece se o Redis cair, as fases e o rollback do rollout, e o prazo da meta de 0,1%. As outras são a evidência para a janela de 24h, o limite de latência, o escopo e os revisores.

**Desvio do template:** adicionei a seção "Alternativas consideradas" entre Proposta e Riscos, porque o template não tem lugar para elas e você descreveu duas descartadas, mais "não fazer nada". A seção diz isso no próprio texto. Se a arquitetura não aceitar seções extras, dá para mover o conteúdo para dentro da Proposta.

Escolhi o ID `DD-2026-001` porque o diretório só tinha o template. Ajuste se já existir uma numeração.
