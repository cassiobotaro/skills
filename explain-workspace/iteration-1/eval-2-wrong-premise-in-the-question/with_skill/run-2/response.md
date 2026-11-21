Python não executa o arquivo linha por linha. Antes de rodar qualquer coisa, ele lê o arquivo inteiro e o compila para bytecode. Só depois executa esse bytecode. O `SyntaxError` aparece na compilação, e nessa hora o `print` da linha 1 ainda não rodou. Como a compilação falhou, a execução nem começa.

Estou supondo que você escreve Python, mas não conhece as etapas internas de execução. Se já conhece, me diga e eu aprofundo.

**O que acontece quando você roda `python arquivo.py`:**
1. O Python lê o arquivo todo e faz o parsing. Aqui ele detecta erros de sintaxe, como parêntese sem fechar, `:` faltando ou indentação inválida.
2. Se o parsing passou, ele gera o bytecode do módulo inteiro.
3. Só então a máquina virtual executa o bytecode, instrução por instrução. É por isso que o Python costuma ser chamado de "interpretado".

Um exemplo com um arquivo de duas linhas:

```python
print("oi")
x = (1 +
```

Isso dá `SyntaxError` e não imprime "oi". Já este arquivo:

```python
print("oi")
print(variavel_inexistente)
```

imprime "oi" e só depois falha com `NameError`. O `NameError` é um erro de execução, e o Python só o descobre ao chegar na linha. O `SyntaxError` é um erro de compilação, e o Python o descobre antes de começar.

**De onde vem a ideia de "linha por linha":** ela é parcialmente verdadeira no REPL, o prompt `>>>`. Ali cada comando digitado é compilado e executado na hora, então o que veio antes já rodou quando você erra. Num arquivo `.py` isso não vale.

Essa explicação vale para o CPython, a implementação padrão. Outras implementações podem diferir nos detalhes. Em todas, porém, os erros de sintaxe aparecem antes da execução.

Um teste para conferir se ficou claro: se a linha 40 tiver uma chamada a uma função que não existe, e não um erro de sintaxe, o `print` da linha 1 roda ou não?

Se você me mostrar o arquivo, eu aponto o que está errado na linha 40.
