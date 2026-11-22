Terminei o documento e estou só confirmando o resultado final. Já passei o `unslop` na prosa.

O doc está em `docs/design/deduplicacao-de-eventos.md`, com as seções do template na ordem original.

**Desvio do template, para você aceitar ou não:** acrescentei uma seção "Alternativas consideradas" entre Proposta e Riscos. O template não tem lugar para as duas alternativas que vocês descartaram (deduplicar no consumidor e idempotência nativa do Kafka), e não quis perdê-las. O restante do esqueleto ficou intacto.

**O que está preenchido, só com o que você disse:**
- Motivação: 4% de duplicatas, reenvio em retry, faturamento inflado, duas reclamações do financeiro.
- Proposta: serviço entre o ingestor e o Kafka, chave idempotente no Redis por 24h, descarte dos repetidos.
- Alternativas: as duas descartadas, cada uma com o motivo que você deu.
- Riscos: só o +5 ms de latência no caminho crítico, registrado como custo aceito.
- Métricas: duplicatas de 4% para abaixo de 0,1%.

**O que ficou como pendência**, cada ponto com uma linha apontando para as Perguntas abertas:
1. Numeração e revisores. Usei DD-2026-001 porque não havia outros docs na pasta. Confirme o número e informe os revisores da arquitetura.
2. Quem gera a chave idempotente e se ela já existe em todos os eventos.
3. O que acontece se o Redis cair, e quais outros riscos e mitigações o time vê.
4. Plano de rollout: fases, critério de avanço e de rollback.
5. Se vocês querem registrar a alternativa "não fazer nada".
6. Se os +5 ms são meta ou só estimativa.
7. O que está fora do escopo.

Não inventei riscos, fases de rollout nem detalhes técnicos que você não mencionou. Também não incluí diagrama, porque a notação pediria tecnologias e protocolos que você não deu. Não fiz commit.
