Vou ir em passos curtos. Você programa em Python há alguns meses, então já conhece funções, listas e `if`. Parto disso e não explico mais nada dessas coisas.

## A ideia de hoje

Uma função recursiva resolve um problema chamando a si mesma para uma versão menor do mesmo problema. Ela precisa de duas partes:

1. **Caso base:** um problema tão pequeno que a resposta é direta.
2. **Passo recursivo:** reduz o problema um pouco e usa a resposta da versão menor para montar a sua.

## Um caso resolvido: somar uma lista

```python
def soma(nums):
    if not nums:                    # caso base: lista vazia
        return 0
    return nums[0] + soma(nums[1:])  # primeiro elemento + soma do resto
```

Para `soma([3, 1, 2])`, o que acontece é:

- `soma([3, 1, 2])` precisa de `3 + soma([1, 2])`
- `soma([1, 2])` precisa de `1 + soma([2])`
- `soma([2])` precisa de `2 + soma([])`
- `soma([])` cai no caso base e devolve `0`

Agora as respostas voltam na ordem inversa: `2 + 0 = 2`, depois `1 + 2 = 3`, depois `3 + 3 = 6`.

Ao escrever o passo recursivo, não tente seguir todas as chamadas de cabeça. Suponha que `soma(nums[1:])` já devolve a resposta certa para a lista menor. Seu trabalho é só dizer como montar a resposta da lista inteira a partir dela. Isso vale para esta função e para a maioria das recursões simples. Em recursões com vários ramos, às vezes você vai precisar traçar as chamadas, mas aí já é um passo à frente.

## Uma pergunta para checar

Se eu apagasse as duas linhas do caso base (`if not nums:` e `return 0`) e chamasse `soma([5])`, o que você acha que aconteceria? Responda com o que você prevê e por quê, mesmo que não tenha certeza.

Depois da sua resposta, escrevemos juntos uma segunda função, e a terceira fica por sua conta.
