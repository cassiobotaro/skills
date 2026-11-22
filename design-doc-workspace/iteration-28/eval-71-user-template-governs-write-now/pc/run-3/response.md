Escrevi o doc em `docs/design/deduplicacao-de-eventos.md`, seguindo o template na ordem, e deixei as perguntas no final. Não fiz commit.

**O que ficou preenchido com o que você disse**
- **Motivação:** os 4% de duplicatas, as duas reclamações do financeiro e o reenvio por retry.
- **Proposta:** o serviço entre o ingestor e o Kafka, guardando a chave idempotente no Redis por 24h e descartando repetidos.
- **Riscos:** só o +5 ms de latência, registrado como custo aceito.
- **Métricas de sucesso:** duplicatas de 4% para abaixo de 0,1%. Marquei os +5 ms como estimativa, não como meta.

**Desvio do template.** Ele não tem lugar para as alternativas que vocês descartaram. Acrescentei a seção "Alternativas consideradas" entre Proposta e Riscos, sem mexer no resto da ordem. O doc diz isso no próprio texto. Se a arquitetura não aceitar a seção extra, é só remover.

**Seções que ficaram como "aguarda resposta"**
- **Riscos:** só o custo de latência está preenchido. Não escrevi outros riscos que você não mencionou, como Redis fora do ar.
- **Plano de rollout:** não tinha nada seu sobre fases ou critério de rollback.

**Perguntas abertas.** São 8:
1. Riscos e mitigações.
2. Rollout.
3. Como medir a taxa de duplicatas, e de onde vem a estimativa de +5 ms.
4. Quem gera a chave idempotente.
5. O que acontece com reenvios depois das 24h.
6. O que fica fora do escopo.
7. O que descarta manter o cenário atual.
8. Revisores e numeração.

Usei **DD-2026-001**, porque `docs/design/` só tinha o template. Confirme se a sequência está certa. O campo Revisores está vazio.

Passei o `unslop` na prosa. Tirei duas frases que afirmavam mais do que você disse: que os consumidores receberiam o fluxo já deduplicado, e que o custo da latência foi aceito "em troca de deduplicar em um único ponto".
