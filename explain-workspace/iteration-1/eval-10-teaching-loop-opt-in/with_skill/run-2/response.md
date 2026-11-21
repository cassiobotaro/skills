Como você já tem Python há alguns meses, vou supor que sabe escrever funções, usar listas e fatiar com `lista[1:]`. Se algum desses ainda está instável, me avise e eu volto um passo.

## Primeira ideia: resolver um problema usando uma versão menor dele mesmo

Recursão é uma função que se chama com um problema menor, até chegar a um caso tão pequeno que a resposta é óbvia. Esse caso óbvio é o **caso base**. Sem ele, a função se chama para sempre.

Um exemplo completo, somar os elementos de uma lista:

```python
def soma(lista):
    if lista == []:                      # caso base: lista vazia soma 0
        return 0
    return lista[0] + soma(lista[1:])    # primeiro elemento + soma do resto
```

Vamos rastrear `soma([2, 5, 1])`. Cada chamada fica esperando a seguinte terminar:

```
soma([2, 5, 1]) = 2 + soma([5, 1])
                      soma([5, 1]) = 5 + soma([1])
                                         soma([1]) = 1 + soma([])
                                                         soma([]) = 0   ← caso base
```

Depois do caso base, as respostas voltam pela cadeia: `1 + 0 = 1`, depois `5 + 1 = 6`, depois `2 + 6 = 8`.

Duas observações:
- Cada chamada recebe uma lista **menor** que a anterior. É isso que garante que a cadeia chega ao caso base.
- Esse `soma` serve só para aprender. Em código real, use `sum()`.

## Sua vez, uma pergunta só

Rastreie `soma([4])`. Quais chamadas acontecem, em que ordem, e qual valor cada uma devolve? Se travar, comece pela pergunta "qual é o `lista[1:]` de `[4]`?".

Quando você responder, o próximo passo é resolvermos juntos um caso novo, e depois você escreve um sozinho.
