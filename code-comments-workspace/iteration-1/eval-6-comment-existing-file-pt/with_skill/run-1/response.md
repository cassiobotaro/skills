Comentei o `cache/ttl.py` em português. O arquivo não tinha nenhum comentário, e o resto do repositório também não, então usei o idioma da conversa. O código não foi alterado, só ganhou comentários e docstrings. Conferi apenas que o arquivo continua com sintaxe Python válida e não rodei testes.

O que ficou documentado:
- **Docstring do módulo:** descreve o propósito do cache. Avisa que ler uma chave não renova a validade (não é LRU, só `put` reinicia o ttl) e que não há trava para acesso concorrente.
- **`MAX_ENTRIES`:** diz o que acontece ao atingir o limite.
- **`__init__`:** explica por que o `clock` é injetável (testes) e por que o padrão é monotônico. Também descreve o formato de `_entries`.
- **`get`:** a entrada expirada só é removida na leitura, então uma chave que nunca mais é lida continua ocupando espaço e contando para o limite. O `>` estrito significa que uma entrada com idade exatamente igual ao ttl ainda vale.
- **`put`:** gravar de novo uma chave existente reinicia o ttl. Com o cache cheio, o despejo remove a entrada mais antiga, mesmo que ela ainda não tenha expirado. Esse despejo percorre todas as entradas (O(n)).

Não consegui estabelecer por que `MAX_ENTRIES` é 1024. Não há issue, teste ou commit que explique, então não escrevi um motivo. Se você ou alguém do time souber (limite de memória, valor arbitrário), vale acrescentar. Quem for ler o arquivo provavelmente vai perguntar isso.

Não alterei nomes, mas sugiro estes dois:
- **`ttl_s`:** o sufixo `_s` já indica segundos e está claro, então pode ficar.
- **`oldest` em `put`:** o nome sugere a entrada mais antiga por gravação, o que é correto. Só tenha em mente que isso não é o mesmo que a "menos usada recentemente".
