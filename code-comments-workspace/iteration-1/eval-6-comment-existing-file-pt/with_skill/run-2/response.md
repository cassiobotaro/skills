Comentei o `cache/ttl.py` em português, porque você escreveu em português e o arquivo não tinha nenhum comentário. Só adicionei comentários e não mudei nenhuma linha de código. Conferi que o arquivo continua com sintaxe válida, mas não rodei o código.

**O que ficou comentado**
- **`TTLCache`:** o que a classe é e dois comportamentos que surpreendem quem lê só a assinatura.
  - A expiração é preguiçosa. Uma entrada vencida só sai ao ser lida ou ao ser expulsa por falta de espaço, e até lá ela ocupa uma vaga.
  - A classe não tem lock, então não serve para várias threads sem sincronização externa.
- **`__init__`:** o contrato do `clock` (função sem argumentos que devolve segundos) e o formato de `_entries`.
- **`get`:**
  - Idade exatamente igual a `ttl_s` ainda é válida, porque a comparação é `>`.
  - Ler não renova o prazo.
  - Uma entrada vencida é removida na leitura.
- **`put`:**
  - Regravar uma chave existente reinicia o prazo e nunca expulsa ninguém.
  - Com o cache cheio e uma chave nova, sai a entrada mais antiga, numa busca linear O(n).

**O que não consegui estabelecer**
- **Por que `MAX_ENTRIES = 1024`:** nada no repositório explica o valor. O comentário diz só o que a constante faz, sem inventar motivo. Se alguém souber a origem (medição, limite de memória, valor arbitrário), vale acrescentar.
- **Por que o `clock` é injetável:** provavelmente é para testes, mas não há nada que confirme. Também ficou fora do comentário.

**Sugestões de renomeação (não apliquei)**
- `ttl_s` → `ttl_seconds`, para quem é novo não ter que adivinhar o sufixo.
- `MAX_ENTRIES` → `MAX_CACHE_ENTRIES`, para ficar claro o que a constante limita quando for importada de outro módulo.
