Comentei o `cache/ttl.py` em português, e o código em si não mudou. Não rodei nada, só adicionei docstrings e comentários.

- **Docstring do módulo:** explica o que o cache faz, e avisa que ele não é thread-safe nem compartilhado entre processos.
- **`MAX_ENTRIES`:** diz que, ao atingir o limite, inserir uma chave nova remove a entrada mais antiga.
- **`__init__`:** descreve `ttl_s` e `clock`, e explica que o `clock` é injetável para os testes simularem o tempo sem `sleep`. Também descreve a estrutura de `_entries`.
- **`get`:** avisa que a expiração é preguiçosa, ou seja, entradas vencidas só saem do cache quando alguém as lê. Também diz que uma entrada com idade exatamente igual ao TTL ainda vale.
- **`put`:** explica que só despeja quando a chave é nova, e que o despejo é pela entrada mais antiga. Isso pode remover uma entrada ainda válida, e a busca é linear, O(n).

Esses comportamentos são os que mais confundem quem chega sem contexto.
