Comentei o `cache/ttl.py` em português. Não rodei nada, e o código em si não mudou: só entraram comentários e docstrings.

O que ficou documentado, pensando em quem está chegando no time:
- **Docstring da classe:** a expiração é "preguiçosa". Uma entrada vencida só sai quando alguém chama `get` na mesma chave, ou quando é despejada em `put`. Não existe limpeza em segundo plano, e a classe não é thread-safe.
- **`clock` injetável:** serve para os testes avançarem o tempo sem `sleep`. O padrão, `time.monotonic`, não é afetado por mudanças no relógio do sistema.
- **`get`:** a entrada só expira quando a idade passa do TTL. Com idade exatamente igual a `ttl_s` ela ainda vale.
- **`put`:** o despejo só acontece com chave nova e cache cheio. Ele remove a entrada gravada há mais tempo, não a menos usada, porque ler não atualiza o instante de gravação. A busca é linear, O(n). Também pode despejar uma entrada ainda válida mesmo havendo outras já vencidas.
- **`MAX_ENTRIES`:** o limite e o que acontece quando ele é atingido.

Essas observações vêm da leitura do código. Vale conferir se o comportamento do despejo é intencional e não um detalhe que o time queira mudar.
