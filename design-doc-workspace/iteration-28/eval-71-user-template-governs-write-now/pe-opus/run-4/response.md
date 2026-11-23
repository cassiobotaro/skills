Escrevi o doc em `docs/design/DD-2026-001-servico-de-deduplicacao-de-eventos.md`. Ele segue o `TEMPLATE.md` na mesma ordem de seções e está com estado **Rascunho**.

**O que está no documento:**
- **Motivação**: os eventos duplicados vêm dos reenvios em retry. Inclui os 4% do mês passado, os relatórios de faturamento inflados e as duas reclamações do financeiro.
- **Proposta**: o serviço fica entre o ingestor e o Kafka, guarda a chave idempotente no Redis por 24h e descarta os repetidos. Uma subseção "Custo aceito" registra o salto a mais no caminho crítico, estimado em +5ms.
- **Métricas de sucesso**: duplicatas de 4% hoje para abaixo de 0,1%.

**Um ponto que foge do template:** ele não tem lugar para alternativas. Para não perder o que vocês discutiram, criei a seção **Alternativas consideradas** logo depois da Proposta, sem mexer no resto da estrutura. Ela traz as duas alternativas que você citou, o serviço escolhido e "não fazer nada", que perde por causa da dor que você descreveu. Se a arquitetura recusar a seção extra, dá para mover esse conteúdo para dentro da Proposta.

**O que ficou para as Perguntas abertas** (você não falou sobre isso, então não inventei nada):
- **Riscos e Plano de rollout** existem como seções, mas só apontam para as perguntas 3 e 4. Uma seção vazia daria a impressão de que ninguém pensou nisso.
- **Revisores** ficou em branco no cabeçalho.
- **Numeração**: não há outros docs no repositório, então usei DD-2026-001. Se a coleção do time fica em outro lugar, o número precisa ser corrigido.
- **Pontos de design:**
  - como os 4% foram medidos e como a meta de 0,1% será medida
  - quem gera a chave idempotente
  - por que a janela é de 24h
  - de onde vem a estimativa de 5ms
  - o que o serviço devolve ao ingestor quando descarta um evento
  - a ordem entre gravar no Redis e publicar no Kafka
  - quem opera o Redis
  - se corrigir os relatórios antigos faz parte do escopo
  - se você quer um diagrama de arquitetura

Quando tiver as respostas, é só mandar que eu incorporo no corpo do documento e tiro a pergunta da lista.
