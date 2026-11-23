Escrevi o doc em `docs/design/deduplicacao-de-eventos.md`, no formato do `TEMPLATE.md`. Ele segue as seções do template, na ordem. O estado é Rascunho, o autor é Rafael Nunes e as datas são de hoje. Não é commit nem PR.

- **ID:** usei `DD-2026-001`, porque `docs/design/` só tinha o template. Se já existe uma sequência fora do repositório, ajuste o número.
- **Desvio do template:** o template não tem lugar para as alternativas que vocês discutiram nem para o trade-off aceito. Criei o bloco "Alternativas consideradas" e o subbloco "Trade-off aceito" dentro de Proposta, antes de Riscos. Mantive as seções e a ordem do template. Se o time de arquitetura não aceitar o bloco extra, ele sai sem afetar o resto.
- **Diagrama:** coloquei só um esboço em texto do fluxo. Um C4 ou um diagrama de sequência exigiria tecnologias e protocolos que você não deu.
- **O que está preenchido:**
  - Motivação, com os 4% de duplicatas e as duas reclamações do financeiro.
  - Proposta: o serviço entre o ingestor e o Kafka, com as chaves no Redis por 24h.
  - As duas alternativas descartadas.
  - A meta de duplicatas abaixo de 0,1%.
  - Os +5ms como custo aceito.
- **O que ficou vazio:** Riscos tem só a latência, e Plano de rollout só aponta para as perguntas abertas. Você não deu nada sobre outros riscos ou fases, então não inventei nada.
- **Perguntas abertas:** são 12. As principais:
  - De onde vem a chave idempotente.
  - O que o serviço faz se o Redis cair.
  - Se consultar e gravar a chave é uma operação atômica.
  - Se a janela de 24h cobre o maior intervalo de retry dos produtores.
  - Como será o rollout e o rollback.
  - Quem são os revisores.

Na alternativa "não fazer nada", escrevi que a discussão não registrou outro raciocínio sobre ela. Se vocês tinham um motivo, complete essa linha.
