Ainda não escrevi o arquivo. O template exige Riscos e Plano de rollout, e a conversa não me deu o conteúdo dessas duas seções. Prefiro não inventar. Preciso de algumas respostas:

1. **Plano de rollout.** Como o serviço entra em produção? Preciso das fases (por exemplo, shadow mode, depois uma parte dos produtores, depois todos), do critério para avançar de uma fase para a próxima e do critério de rollback.
2. **Riscos.** O único que você me deu foi o +5ms de latência no caminho crítico. Que outros riscos o time viu, e qual é a mitigação de cada um? Os principais que eu esperaria são:
   - o que acontece com a ingestão se o Redis cair (falha aberta, aceitando duplicatas, ou falha fechada);
   - o que acontece se o próprio serviço de dedup cair ou degradar;
   - o que acontece com um retry que chega depois das 24h.
   
   Se o time não discutiu algum deles, posso registrá-lo em Perguntas abertas.
3. **Métricas de sucesso.** A meta é duplicatas abaixo de 0,1%, com 4% de base. Há alguma meta de latência além dos +5ms estimados, como p99 ou um teto aceitável? E como vocês medem a taxa de duplicatas hoje?
4. **Revisores e numeração.** Quem são os revisores, ou deixo o campo vazio? Como `docs/design/` só tem o template, vou usar `DD-2026-001`. Confirma?
5. **Chave idempotente.** Quem gera a chave: o produtor ou o ingestor? Se o time ainda não definiu, registro em Perguntas abertas.

O template não tem lugar para as alternativas que você descreveu (dedup no consumidor e idempotência nativa do Kafka) nem para as metas. Vou acrescentar uma seção "Alternativas consideradas", dentro de ou logo após Proposta, mantendo as seções do template na ordem original. Aviso porque é um desvio do formato, e você decide se o time de arquitetura aceita assim.
