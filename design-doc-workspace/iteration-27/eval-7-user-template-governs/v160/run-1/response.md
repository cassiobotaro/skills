Ainda não escrevi o arquivo. Faltam três seções do template que a conversa não preencheu, e prefiro não inventar conteúdo nelas. Antes, duas observações.

- **Numeração:** `docs/design/` só tem o `TEMPLATE.md`, então não há precedente de sequência. Pelo template, o ID é `DD-2026-<seq>`. Vou usar `DD-2026-001`, a menos que você tenha outro número.
- **Alternativas e metas:** o template não tem seção para alternativas nem para metas. Vou manter a ordem e os títulos do template e incluir as duas alternativas descartadas dentro de **Proposta**, como subseção. Aviso porque isso é um desvio pequeno do formato, e o time de arquitetura pode preferir outro lugar.

O que já tenho, vindo da sua mensagem:
- **Motivação:** 4% de duplicatas no mês passado, reenvio em retry dos produtores, relatórios de faturamento inflados e duas reclamações do financeiro.
- **Proposta:** serviço entre o ingestor e o Kafka, com chave idempotente no Redis por 24h e descarte dos repetidos.
- **Alternativas descartadas:** deduplicar no consumidor e usar a idempotência nativa do produtor Kafka.
- **Trade-off aceito:** mais um salto no caminho crítico, com cerca de +5ms de latência.
- **Meta:** duplicatas abaixo de 0,1%.

Preciso destas respostas:

1. **Riscos:** além dos +5ms, o que pode dar errado? Por exemplo:
   - Se o Redis cair ou ficar lento, o serviço falha aberto (deixa passar duplicatas) ou fechado (bloqueia a ingestão)?
   - Como o serviço trata a janela entre gravar a chave e publicar no Kafka?
   - Como ele evita ser um ponto único de falha?
   - Como o time pretende mitigar cada risco?
2. **Plano de rollout:** quais são as fases (shadow mode, percentual de tráfego, por produtor)? Qual critério faz avançar de uma fase para a próxima? Qual gatilho e qual procedimento levam ao rollback?
3. **Métricas de sucesso:** além de duplicatas abaixo de 0,1%, existe teto para a latência adicionada (os 5ms são estimativa ou limite)? Como a taxa de duplicatas vai ser medida, e sobre qual janela?
4. **Proposta (detalhes):**
   - De onde vem a chave idempotente: o produtor envia, ou o serviço a deriva do payload?
   - Quem é dono do serviço?
   - Você quer um diagrama de arquitetura (C4) e um de sequência do fluxo? Se quiser, preciso saber a tecnologia do ingestor e o protocolo entre os componentes. Não vou presumir isso.
5. **Cabeçalho:** quem são os revisores? Se ainda não houver, deixo o campo em branco.

Se alguma resposta ainda não existir, diga e eu a registro em **Perguntas abertas**. Passo a ser uma pergunta em aberto, e não uma afirmação no corpo do doc.
