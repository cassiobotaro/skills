Rafael, o doc está em `docs/design/deduplicacao-de-eventos.md`, no estado Rascunho e com você como autor. Não rodei a skill `unslop`, então o texto não passou por essa revisão.

Segui o `TEMPLATE.md` na ordem e com os cabeçalhos originais. Só preenchi o que você disse. Ficaram pendentes o número do documento (`DD-2026-<seq>` ainda sem sequência) e os revisores.

**Desvio do template:** o template não tem lugar para as alternativas que vocês discutiram nem para o trade-off aceito. Criei duas seções extras, "Alternativas consideradas" e "Trade-offs aceitos", entre Proposta e Riscos. O resto do esqueleto continua igual. Se a arquitetura só aceita o formato exato, mova esse conteúdo para dentro de Proposta.

**O que cada seção traz:**
- **Motivação:** os 4% de duplicatas no mês passado, o reenvio por retry e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave guardada no Redis por 24h.
- **Alternativas consideradas:** não fazer nada, deduplicar no consumidor e a idempotência nativa do Kafka, cada uma com o motivo do descarte.
- **Trade-offs aceitos:** o salto a mais na ingestão, com +5 ms estimados.
- **Riscos:** só a latência, porque foi o único risco que você citou.
- **Plano de rollout:** só aponta para as perguntas abertas.
- **Métricas de sucesso:** meta de duplicatas abaixo de 0,1%, partindo de 4%.

Não inventei nada para preencher as lacunas. Também não fiz diagrama, porque o Redis e o Kafka como tecnologias nas caixas já estariam definidos, mas o fluxo em si você não detalhou.

**Perguntas para o final do doc (seção Perguntas abertas):**
1. Qual é o número sequencial do DD e quem são os revisores, de quais áreas?
2. Quais são os riscos além da latência? Em especial, o que acontece se o Redis cair ou perder dados: o serviço deixa o evento passar ou bloqueia?
3. Como é o rollout: fases, critério para avançar e plano de rollback?
4. De onde vem a chave idempotente: dos produtores ou calculada pelo ingestor?
5. Como e onde a taxa de duplicatas será medida, e em que prazo se espera chegar a 0,1%?
6. O que fica fora de escopo?
7. Por que 24h? Duplicata que chegar depois da janela passa, e o time aceita isso?
