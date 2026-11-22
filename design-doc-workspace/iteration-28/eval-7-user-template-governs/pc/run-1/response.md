Ainda não criei o arquivo. O template exige seções que a conversa não preencheu, e eu não vou inventar esse conteúdo. Você já me deu Motivação, a Proposta, as duas alternativas descartadas, o trade-off dos +5ms e a meta de 0,1%. Faltam estas respostas:

1. **Riscos.** Além dos +5ms, o que pode dar errado e como mitigamos? Preciso principalmente de duas decisões:
   - Se o Redis cair ou ficar lento, o serviço deixa passar eventos (aceita duplicata) ou bloqueia a ingestão?
   - O que acontece quando o próprio serviço de dedup cai, já que ele entra no caminho crítico?
2. **Plano de rollout.** Quais são as fases (por exemplo, sombra, percentual do tráfego, 100%)? Qual critério faz avançar de uma fase para a outra e qual dispara rollback?
3. **Métricas de sucesso.** A meta é duplicatas abaixo de 0,1%, medida a partir dos 4% atuais. Você tem também um teto para a latência (os +5ms são estimativa ou limite)? E como vamos medir a taxa de duplicatas?
4. **Perguntas abertas.** O que ainda está em aberto? Dois candidatos que me ocorreram, mas que são seus para confirmar:
   - Qual é a chave idempotente e quem a gera?
   - O que acontece com duplicatas que chegam depois de 24h?
5. **Cabeçalho.** Quem são os revisores? E o número da sequência: `docs/design/` só tem o template, então posso usar `DD-2026-001`?

**Estrutura.** Vou seguir o template na ordem e com os mesmos títulos. As alternativas descartadas (dedup no consumidor e idempotência nativa do Kafka) e os objetivos/fora de escopo entram como subseções dentro de **Proposta**, sem criar seção de nível superior nova. Assim o formato que a arquitetura exige fica intacto.

Se preferir o documento já, com as seções sem resposta marcadas como pendentes e listadas em Perguntas abertas, é só avisar.
