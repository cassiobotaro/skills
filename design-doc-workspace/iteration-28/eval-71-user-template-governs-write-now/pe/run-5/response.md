Salvei o design doc em `docs/design/deduplicacao-de-eventos.md`, como DD-2026-001 (era o primeiro, já que `docs/design/` só tinha o template). O estado é Rascunho, com você como autor e a data de hoje. Não rodei nenhum teste nem revisão de prosa além da minha leitura.

**Como ficou o doc**
- As seções do template estão todas, na ordem original: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.
- A Motivação traz os 4% de duplicatas e as duas reclamações do financeiro.
- A Proposta descreve o fluxo, com um diagrama simples de componentes (Produtores, Ingestor, Serviço de deduplicação, Redis, Kafka) e o texto explicando.
- O custo aceito de +5 ms está na Proposta e na tabela de Riscos.
- As Métricas de sucesso têm 4% como base e abaixo de 0,1% como meta.

**Um desvio do template**
O template não tem lugar para alternativas, e as duas que vocês descartaram (deduplicar no consumidor e idempotência nativa do Kafka) não podiam sumir. Coloquei uma subseção "Alternativas consideradas" dentro da Proposta, sem mudar o esqueleto. A subseção abre com uma frase explicando que o template não tem essa seção. Se o time de arquitetura for rígido com isso, tire a frase ou mova as alternativas para onde eles preferirem.

**O que ficou em aberto**
Você só deu uma mitigação (nenhuma, para a latência), então não inventei riscos nem rollout.
- **Riscos:** a tabela tem só a latência. Os demais riscos viraram perguntas, como Redis indisponível e reenvio depois das 24 h.
- **Plano de rollout:** a seção só aponta para as Perguntas abertas.
- **Perguntas abertas:** são 12, agrupadas por tema. Duas valem atenção antes de mandar para revisão:
  - Quem gera a chave idempotente.
  - A ordem entre gravar no Redis e publicar no Kafka, que define se uma falha no meio perde ou duplica o evento.

A lista também pergunta quem revisa o doc e se "fazer nada" foi avaliado. O campo Revisores ficou vazio.

Não fiz commit.
