A premissa está um pouco imprecisa: o Python **não** executa o arquivo linha por linha. Ele trabalha em duas fases.

**1. Compilação (o arquivo inteiro)**
Antes de rodar qualquer coisa, o CPython lê o arquivo todo, faz o parse e compila tudo para bytecode. É nessa fase que o `SyntaxError` aparece. Se a linha 40 tem um erro de sintaxe, o parse falha e o programa nem começa. Por isso o `print` da linha 1 nunca chega a executar.

**2. Execução (o bytecode)**
Só depois que a compilação termina sem erros é que a máquina virtual executa o bytecode, instrução por instrução. É nessa fase que aparecem os erros de execução, como `NameError`, `ZeroDivisionError` e `TypeError`. Esses sim acontecem no meio do programa, depois de as linhas anteriores terem rodado.

**Exemplo**

```python
print("oi")      # nunca roda
x = (1 +         # SyntaxError: '(' was never closed
```

```python
print("oi")      # roda
y = 1 / 0        # ZeroDivisionError só na hora de executar
```

No primeiro caso, nada é impresso. No segundo, o "oi" aparece e só depois vem o erro.

**De onde vem a ideia de "linha por linha"?**
Vem de duas coisas:
- O **REPL** (o prompt `>>>`) compila e executa cada comando separadamente. Lá o comportamento parece mesmo linha por linha.
- O Python não gera um executável nativo, e "interpretado" acabou virando sinônimo de "lê e executa uma linha de cada vez". Na prática, o CPython compila para bytecode e o interpreta.

**Observação**
O `SyntaxError` só pega erros de *sintaxe*. Erros de nome ou de tipo continuam aparecendo apenas em tempo de execução. Para o parser, `print(variavel_inexistente)` é um código válido.

Se quiser ver a fase de compilação separada, rode `python -m py_compile arquivo.py`. Ele só compila e reporta erros de sintaxe, sem executar nada.
