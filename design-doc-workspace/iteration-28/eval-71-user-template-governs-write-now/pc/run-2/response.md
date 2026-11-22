O design doc está salvo em `docs/design/deduplicacao-de-eventos.md`, com as seções do template na ordem original. Não fiz commit.

**O que entrou, só com o que você disse**
- **Motivação:** 4% de duplicatas no mês passado e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave guardada no Redis por 24h e o descarte de repetidos. O custo de +5 ms aparece como estimativa.
- **Métricas:** duplicatas abaixo de 0,1%, com 4% como linha de base.

**Desvio do template**
Ele não tem lugar para as alternativas que vocês discutiram, então criei a seção "Alternativas consideradas" entre Proposta e Riscos. Isso é um desvio do formato, e o time de arquitetura precisa aceitá-lo. Se não aceitar, o conteúdo pode ir para dentro da Proposta.

**Seções sem conteúdo ainda**
- **Revisores:** ficou como "Aguardando resposta".
- **Riscos:** só tem a latência. O restante aguarda a pergunta 4.
- **Plano de rollout:** só uma linha apontando para a pergunta 6.
- **Métricas de sucesso:** além da meta de duplicatas, o resto aguarda a pergunta 7.

**Perguntas abertas** (estão no final do doc)
1. Quem revisa o doc e quais outros times são impactados?
2. Quem gera a chave idempotente, o produtor ou o ingestor? Todos os produtores enviam uma chave estável entre retries?
3. O serviço grava a chave no Redis antes ou depois de publicar no Kafka? Se o Kafka falhar depois de a chave ser gravada, o retry seria descartado e o evento se perderia.
4. O que acontece se o Redis cair? Há outros riscos que o time já identificou?
5. Por que descartar "não fazer nada", além do impacto no faturamento?
6. Como é o rollout, com fases e critérios de avanço e de rollback?
7. Quais métricas acompanhamos além da taxa de duplicatas, por exemplo latência p99 e taxa de descarte, e com quais limites?
8. A numeração **DD-2026-001** é um chute meu, porque `docs/design/` só tem o template. Confirme qual é a sequência certa.
9. Por que 24 horas? Existe um dado sobre o intervalo máximo entre um evento e seus reenvios?

Passei o unslop no texto e removi duas afirmações que eu tinha inferido e você não tinha dito. Não pus diagrama, porque a ordem entre gravar a chave e publicar (pergunta 3) ainda está em aberto. Posso adicionar um quando você responder.
