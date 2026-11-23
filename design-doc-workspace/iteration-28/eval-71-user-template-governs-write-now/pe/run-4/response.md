Escrevi o doc em `docs/design/deduplicacao-de-eventos.md`, no formato do `TEMPLATE.md`. Ele segue as mesmas seções e a mesma ordem, e o estado é Rascunho. Não rodei o `unslop` nem uma revisão ortográfica separada.

**O que ficou preenchido, só com o que você disse:**
- **Motivação:** os 4% de duplicatas no mês passado, o reenvio em retry e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, guardando a chave no Redis por 24h e descartando os repetidos.
- **Riscos:** só os +5ms de latência no caminho crítico, registrado como custo aceito.
- **Métricas de sucesso:** duplicatas abaixo de 0,1%, com os 4% como ponto de partida.

**Desvio do template:** ele não tem lugar para as alternativas. Mantive a estrutura e acrescentei uma seção "Alternativas consideradas" logo depois da Proposta, com a deduplicação no consumidor e a idempotência nativa do produtor Kafka, cada uma com o motivo do descarte. Se o time de arquitetura não aceitar a seção extra, é fácil mover esse conteúdo para dentro da Proposta.

**Plano de rollout:** ficou como "A definir", porque você não deu nada sobre fases, critério de avanço ou rollback.

**Não inventei riscos nem mitigações.** Vi falhas óbvias no desenho, como o Redis cair ou um reenvio chegar depois das 24h, mas só você pode dizer se elas contam como risco. Por isso viraram perguntas em Perguntas abertas. São 12 no total, e entre elas:
- quem gera a chave idempotente;
- o que o serviço faz quando o Redis falha;
- se a verificação e o registro da chave precisam ser atômicos;
- o que acontece com um reenvio depois das 24h;
- se os +5ms são estimativa ou medição;
- como será o rollout.

**Campos a conferir:**
- **Revisores:** deixei em branco.
- **Número DD-2026-001:** é um palpite meu, porque `docs/design/` só tinha o template. Confirme o número certo com o time de arquitetura.
- **Datas:** usei 2026-11-23.
