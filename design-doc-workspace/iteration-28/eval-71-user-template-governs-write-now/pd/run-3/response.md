Salvei o doc em `docs/design/servico-de-deduplicacao-de-eventos.md`, no estado Rascunho. Usei só o que você me disse, e as lacunas viraram perguntas abertas.

**Fidelidade ao template:** mantive as seções do `TEMPLATE.md` na mesma ordem. Fiz um desvio e ele é seu para aceitar ou tirar. O template não tem lugar para as alternativas, então criei a seção "Alternativas consideradas" entre Proposta e Riscos. Ela traz as duas que vocês descartaram e o "não fazer nada".

**O que está no doc:**
- **Motivação:** os 4% de duplicatas no mês passado, o faturamento inflado e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave idempotente guardada no Redis por 24h e os repetidos descartados.
- **Riscos:** só o +5 ms de latência, que o time aceitou.
- **Métricas de sucesso:** duplicatas de 4% para menos de 0,1%, e a latência de +5 ms marcada como estimativa.
- **Plano de rollout:** só um ponteiro para as perguntas abertas, porque você não me deu as fases nem os critérios de avanço e de rollback.

**Sem diagrama:** o template pede diagramas, mas um desenho exigiria detalhes que você não deu. Entre eles estão a origem da chave e o que acontece com o Redis fora do ar. Quando você responder, dá para adicionar um.

**Perguntas abertas (10, no fim do doc):**
1. Quem gera a chave idempotente e de quais campos ela é composta?
2. O que o serviço faz quando o Redis está indisponível: deixa passar ou rejeita?
3. A chave é registrada antes ou depois de publicar no Kafka?
4. Por que 24h? E o que acontece com duplicatas que chegam depois disso?
5. Que outros riscos existem além da latência, e qual a mitigação de cada um?
6. Como é o rollout: fases, critério de avanço e critério de rollback?
7. Qual é a latência de hoje, e existe um limite que invalidaria a proposta?
8. Como se mede a taxa de duplicatas, e em que prazo a meta de 0,1% deve ser atingida?
9. O que fica fora do escopo?
10. Quem são os revisores?

**Confirmar:** usei o número DD-2026-001 porque `docs/design/` só tinha o template. Se já existem DDs em outro lugar, o número precisa mudar. O campo **Revisores** ficou em branco pelo mesmo motivo.

Não rodei o `unslop` porque ele não está entre as skills disponíveis aqui.
