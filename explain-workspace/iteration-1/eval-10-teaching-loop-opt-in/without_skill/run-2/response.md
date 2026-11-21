# Recursão, passo 1: a ideia central

Como você já programa em Python, vou pular o básico de sintaxe. Vou ensinar em etapas curtas e, no fim de cada uma, te dar um exercício. Responda e eu sigo para a próxima etapa.

## A ideia

Uma função recursiva resolve um problema chamando **a si mesma** para uma versão **menor** do mesmo problema. Ela precisa de duas partes:

1. **Caso base:** o caso tão pequeno que você responde direto, sem chamar ninguém.
2. **Passo recursivo:** reduz o problema e confia que a chamada recursiva resolve o menor. Depois você usa essa resposta para montar a sua.

Exemplo: somar os números de 1 até `n`.

```python
def soma(n):
    if n == 0:          # caso base
        return 0
    return n + soma(n - 1)   # passo recursivo
```

## Como pensar (isto é o que separa entender de decorar)

Não tente simular todas as chamadas de cabeça. Faça o **salto de fé**:

> "Suponha que `soma(n - 1)` já devolve a resposta certa. Com isso, como eu obtenho `soma(n)`?"

Resposta: `n + soma(n - 1)`. Se o caso base está certo e cada passo aproxima o problema do caso base, a função está correta. Isso é indução matemática aplicada a código.

## Veja a pilha uma vez

Rastreie `soma(3)`:

```
soma(3) = 3 + soma(2)
              soma(2) = 2 + soma(1)
                          soma(1) = 1 + soma(0)
                                      soma(0) = 0      ← caso base
                          soma(1) = 1 + 0 = 1
              soma(2) = 2 + 1 = 3
soma(3) = 3 + 3 = 6
```

As chamadas vão **descendo** até o caso base. Depois os resultados **sobem** e cada chamada completa o seu cálculo.

## Teste rápido

**Pergunta 1 (prever, sem rodar):** o que acontece com esta função? Por quê?

```python
def soma_errada(n):
    return n + soma_errada(n - 1)
```

**Pergunta 2 (prever):** o que `soma(-1)` faz na função `soma` do exemplo? Como você consertaria?

**Exercício 3 (escrever):** escreva `fatorial(n)` recursivo. Antes do código, escreva em uma frase qual é o caso base e qual é o salto de fé.

**Exercício 4 (um pouco mais difícil):** escreva `tamanho(lista)`, que devolve o tamanho de uma lista **sem usar `len`**. Dica: pense em `lista[1:]` como "a lista menor".

Mande as respostas, mesmo que erradas. Os erros me mostram onde ajustar a explicação. Na próxima etapa corrijo suas respostas e passamos para recursão sobre listas e strings, e depois para o porquê de `fibonacci` ingênuo ser lento.
