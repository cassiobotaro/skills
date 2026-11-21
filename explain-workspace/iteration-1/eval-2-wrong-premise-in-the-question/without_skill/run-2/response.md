A premissa está um pouco errada: o Python não executa o arquivo "linha por linha" do jeito que parece. O que ele faz é **compilar o arquivo inteiro antes de executar qualquer coisa**.

**O que acontece quando você roda `python arquivo.py`:**

1. **Tokenização e parsing:** o Python lê o arquivo *inteiro* e constrói a árvore sintática (AST). É aqui que o `SyntaxError` aparece. Se a linha 40 tem um erro de sintaxe, o parser falha nesse ponto, e nada foi executado ainda.
2. **Compilação para bytecode:** a AST vira bytecode.
3. **Execução:** só então a máquina virtual (a PVM) executa o bytecode, instrução por instrução. É só nessa etapa que o `print` da linha 1 rodaria.

Por isso o `print` da linha 1 nunca chega a rodar: o programa nem começou.

**Exemplo:**

```python
print("oi")      # linha 1
x = = 3          # linha 2: SyntaxError
```

Rodando isso, você vê só o `SyntaxError`. O "oi" não aparece.

**Então em que sentido o Python é "interpretado"?**
Ele é interpretado no sentido de que não gera um executável nativo: o bytecode é executado por uma VM, sem passo separado de compilação que você precise rodar. Mas isso não significa processar o texto linha a linha. Existe compilação, só que implícita e feita em memória (por isso os arquivos `.pyc`).

**Contraste: erros em tempo de execução**
Erros como `NameError`, `ZeroDivisionError` ou `TypeError` só aparecem quando a linha é executada. Nesse caso o `print` da linha 1 roda normalmente antes de o erro estourar na linha 40:

```python
print("oi")      # roda
print(1 / 0)     # ZeroDivisionError só aqui
```

**Onde a ideia de "linha por linha" vale:**
- No **REPL** (`python` interativo), cada instrução digitada é compilada e executada separadamente. Lá, um erro de sintaxe só afeta aquela instrução.
- Com `exec()`/`eval()` ou `import`, cada trecho ou módulo é compilado como uma unidade própria. Um `import` de módulo com erro de sintaxe falha no momento do import, não antes.

**Resumo:** `SyntaxError` é detectado na fase de *parsing*, que olha o arquivo todo antes de executar qualquer coisa. Erros de execução só aparecem quando a linha é de fato executada.
