Li o template e o que você contou. Ainda não criei o arquivo, porque o template exige conteúdo em seções que a conversa não preencheu. Prefiro perguntar a inventar. Não há outros design docs no repositório, então o documento será o `DD-2026-001`, em `docs/design/`.

**Já tenho o suficiente para:**
- **Motivação:** 4% de duplicatas no mês passado por reenvio em retry, faturamento inflado e duas reclamações do financeiro.
- **Proposta (núcleo):** serviço entre o ingestor e o Kafka, com a chave idempotente no Redis por 24h e descarte dos repetidos.
- **Trade-off aceito:** mais um salto no caminho crítico, com cerca de +5ms.
- **Métricas:** duplicatas abaixo de 0,1%.
- **Alternativas:** dedup no consumidor e idempotência nativa do produtor Kafka. O template não tem seção para elas. Vou criar uma seção "Alternativas consideradas" dentro de Proposta, sem mudar a ordem nem os títulos do template. Se preferir outro lugar, me diga.

**Preciso de você para completar:**

1. **Riscos:** o que a equipe discutiu que pode dar errado, e como pretende mitigar? Só o +5ms foi dito, e não vou escrever riscos que ninguém levantou.
2. **Plano de rollout:** quais são as fases (por exemplo, sombra, percentual de produtores, total)? Qual critério faz avançar de fase e qual dispara rollback?
3. **Proposta:**
   - Qual é a chave idempotente? É um ID gerado pelo produtor, ou um hash de campos do evento?
   - O diagrama de componentes precisa de tecnologia e protocolo em cada caixa e seta. Qual é a tecnologia do ingestor e do novo serviço, e como eles se comunicam?
4. **Métricas:** além de duplicatas < 0,1%, há meta para a latência (o +5ms é um teto)? Como e onde vocês medem a taxa de duplicatas?
5. **Perguntas abertas e cabeçalho:** o que ainda está em aberto? Quem são os revisores, ou deixo em branco?

Se alguma resposta for "ainda não sabemos", registro como pergunta aberta. Para Riscos e Rollout isso também vale. Prefiro isso a um texto genérico.
