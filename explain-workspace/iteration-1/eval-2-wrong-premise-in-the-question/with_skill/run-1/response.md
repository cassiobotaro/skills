A premissa está errada: o Python não executa linha por linha. Antes de rodar qualquer coisa, o CPython lê o arquivo inteiro e o compila para bytecode. Só depois a máquina virtual executa esse bytecode. O `SyntaxError` aparece na compilação, e nessa hora o `print` da linha 1 ainda não rodou.

Estou assumindo que você já escreve Python e só ficou com essa ideia de "interpretado = linha por linha".

Um exemplo que eu montei, sem rodar:

```python
print("oi")      # linha 1
x = 1
if x == 1        # linha 3: falta o ":"
    print("um")
```

1. O Python analisa o arquivo todo e monta uma árvore sintática.
2. Na linha 3 a árvore não fecha, então ele levanta `SyntaxError` e para.
3. Nada chegou a ser executado, então "oi" não aparece.

Se o erro fosse de execução, como `print(y)` com `y` indefinido na linha 3, o "oi" apareceria antes. Esse erro só existe quando a linha roda. Um erro de sintaxe existe desde a leitura do arquivo.

"Interpretado" descreve a implementação: o Python roda bytecode numa máquina virtual, sem gerar um executável nativo. Não quer dizer que cada linha de texto é lida e executada isoladamente. Um caso parecido com o que você imaginou é o REPL (o prompt `>>>`), que compila e executa uma instrução por vez. Por isso lá os erros de sintaxe aparecem só na instrução em que ocorrem.

Uma checagem: o arquivo `a.py` tem `print("a")` e depois `import b`, e `b.py` tem um erro de sintaxe na linha 1. O "a" aparece antes do erro ou não? Responda com base no que descrevi acima.
