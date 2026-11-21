# Recursão, aos poucos

Vamos em passos curtos. Você responde, eu corrijo e só então avanço. Começamos pela ideia central, sem código complicado.

## Passo 1: a ideia

Recursão é resolver um problema usando a solução de **uma versão menor do mesmo problema**.

Exemplo do dia a dia: você está numa fila e quer saber sua posição. Pergunta para a pessoa da frente: "qual é a sua posição?". Ela pergunta para a da frente dela, e assim por diante. A primeira da fila responde "1". Cada pessoa soma 1 à resposta que recebeu e devolve.

Toda função recursiva precisa de duas partes:

1. **Caso base**: o caso tão simples que dá para responder direto. É a primeira pessoa da fila, que diz "1".
2. **Passo recursivo**: reduz o problema e chama a si mesma, usando o resultado para montar a resposta.

Sem caso base, a função nunca para. O Python interrompe com `RecursionError`.

## Passo 2: o primeiro código

```python
def contagem_regressiva(n):
    if n == 0:              # caso base
        print("Fim!")
        return
    print(n)
    contagem_regressiva(n - 1)   # passo recursivo: problema menor
```

`contagem_regressiva(3)` imprime `3`, `2`, `1`, `Fim!`.

Repare que `n - 1` aproxima a chamada do caso base. Se o argumento não chegasse perto do caso base, a recursão não terminaria.

## Teste 1 (responda antes de eu continuar)

**a)** O que `contagem_regressiva(2)` imprime? Escreva a saída, linha por linha.

**b)** O que acontece se eu apagar o `if n == 0` e chamar `contagem_regressiva(3)`? Por quê?

**c)** Com suas palavras, qual é o caso base e qual é o passo recursivo na função acima?

Responda com o que você pensa, mesmo que esteja inseguro. Errar aqui é útil, porque mostra onde ajustar a explicação.

## O que vem depois

Dependendo das suas respostas, o plano é:

- **Passo 3**: funções que *devolvem* valores, como fatorial e soma de lista. É aqui que a maioria das pessoas trava.
- **Passo 4**: rastrear a pilha de chamadas à mão, para ver o que acontece "na volta" da recursão.
- **Passo 5**: problemas com mais de uma chamada recursiva (Fibonacci, percorrer pastas, subconjuntos), e quando recursão é uma má ideia (custo e limite de profundidade).

Manda suas respostas do Teste 1 quando puder.
