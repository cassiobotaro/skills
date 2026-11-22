Escrevi o design doc em `docs/design/dd-2026-001-deduplicacao-de-eventos.md`, seguindo as seções do template na ordem. Não rodei nada além da escrita e das edições do unslop. Não renderizei nem validei o Markdown.

**O que o doc cobre**
- **Motivação:** os 4% de duplicatas no mês passado, o reenvio em retry e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave idempotente no Redis por 24h e o descarte de repetidos.
- **Riscos:** o custo aceito de +5 ms no caminho crítico, dito como estimativa sem medição.
- **Métricas de sucesso:** duplicatas abaixo de 0,1%, com a linha de base de 4%.

**Desvio do template:** acrescentei a seção "Alternativas consideradas", entre Proposta e Riscos. O template não tem lugar para as duas alternativas que vocês descartaram, nem para "não fazer nada". O resto da estrutura ficou como estava. Se a arquitetura não aceitar a seção extra, é só remover.

**Perguntas abertas:** são 14, agrupadas em Rollout, Riscos, Proposta e Contexto e processo. As mais importantes:
- **Plano de rollout:** você não deu nada sobre fases, critérios de avanço ou rollback. A seção diz só que não está definido e aponta para as perguntas.
- **Falha do Redis:** o que acontece com a ingestão se ele cair ou perder chaves antes das 24h.
- **Chave idempotente:** quem a gera e se todos os produtores já a enviam.
- **Janela de 24h:** quanto das duplicatas atuais chega depois dela.
- **Medição da meta de 0,1%:** como ela será medida.
- **Revisores:** o campo ficou vazio, e a pergunta 12 pede as equipes afetadas.
- **Fora de escopo:** não ficou registrado, porque você não definiu.

**Para conferir**
- O número **DD-2026-001** é suposição minha, porque não havia outro doc em `docs/design/`. Se já existe uma numeração, ajuste o título, a tabela e o nome do arquivo.
- Passei o unslop na prosa. Ele me fez tirar duas afirmações que eu tinha escrito sem você ter dito: que hoje nenhuma etapa descarta duplicatas, e que os consumidores passariam a receber um fluxo sem repetidos.
- Também tirei um limite de latência que eu tinha posto nas métricas. Você deu +5 ms só como estimativa, então a métrica agora compara a medição com ela e a pergunta 6 pede o limite real.

Não fiz commit.
