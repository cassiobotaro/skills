**Um mutex (de *mutual exclusion*) é um cadeado: só uma goroutine por vez pode estar na parte do código que ele protege, e as outras esperam.**

Vou assumir que você conhece `async/await` e o event loop do JavaScript, mas não threads nem concorrência paralela. Se já souber, me diga e eu ajusto.

**Por que isso não existia no seu JavaScript**

O JS roda o seu código em uma thread só. Entre um `await` e outro, nada mais mexe nas suas variáveis. Em Go, goroutines podem rodar ao mesmo tempo em núcleos diferentes. Duas delas podem mexer na mesma variável no mesmo instante, e o resultado fica errado.

**Um caso concreto**

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	contador := 0
	var wg sync.WaitGroup

	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			contador++ // sem proteção
		}()
	}

	wg.Wait()
	fmt.Println(contador) // quase nunca é 1000
}
```

`contador++` parece uma operação só, mas são três passos: ler o valor, somar 1 e gravar. Suponha que duas goroutines leiam `7` ao mesmo tempo. As duas gravam `8`, e um incremento se perdeu. Isso se chama *data race*.

Com um mutex, só uma goroutine por vez executa o trecho entre `Lock` e `Unlock`:

```go
var mu sync.Mutex
contador := 0

// dentro de cada goroutine:
mu.Lock()
contador++
mu.Unlock()
```

Agora o resultado é sempre 1000. As goroutines passam pelo incremento uma de cada vez. Você perde um pouco de velocidade nesse trecho, e só nele.

**Como se usa na prática**

- O mutex fica junto do dado que protege, normalmente numa struct, e todo acesso a esse dado passa por `Lock`/`Unlock`.
- O costume é usar `defer mu.Unlock()` logo depois do `Lock()`, para o cadeado ser liberado mesmo se a função sair cedo.
- Esquecer o `Unlock` trava as outras goroutines para sempre (*deadlock*).
- Você pode achar data races com `go run -race` ou `go test -race`.

**O que esta versão deixa de fora**

Existem `sync.RWMutex` (muitos leitores ou um escritor), `sync/atomic` (para um contador simples como o do exemplo) e canais, que são a alternativa idiomática em Go quando você quer passar dados entre goroutines em vez de compartilhá-los. Vale olhar isso quando seu caso for mais que "proteger uma variável".

**Uma pergunta para conferir**

Se eu tirar o `Lock`/`Unlock` e rodar o programa com 2 goroutines em vez de 1000, o resultado pode dar errado? E se eu rodar com 1000 goroutines, mas com `GOMAXPROCS=1`? Pense um pouco antes de responder.
