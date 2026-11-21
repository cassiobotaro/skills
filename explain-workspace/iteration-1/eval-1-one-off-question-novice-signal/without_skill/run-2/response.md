Um **mutex** (de *mutual exclusion*, exclusão mútua) é um "cadeado" que garante que só **uma goroutine por vez** mexa em um dado compartilhado.

## Por que isso importa em Go (e não no JS)

No JavaScript você quase nunca precisa disso. Seu código roda em uma única thread, com event loop. Entre um `await` e outro, ninguém mexe nas suas variáveis.

Em Go, goroutines rodam **de verdade em paralelo**, em várias threads do sistema. Se duas delas alteram a mesma variável ao mesmo tempo, você tem uma *race condition*:

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
			contador++ // PERIGO: ler, somar e escrever não é atômico
		}()
	}

	wg.Wait()
	fmt.Println(contador) // esperado 1000, mas pode dar 937, 981...
}
```

O `contador++` são três passos (ler, somar, gravar). Duas goroutines podem ler o mesmo valor, e uma atualização se perde.

## A solução: `sync.Mutex`

```go
var mu sync.Mutex
contador := 0

// dentro de cada goroutine:
mu.Lock()    // "pego a chave"; se outra goroutine está com ela, espero
contador++
mu.Unlock()  // "devolvo a chave"
```

Agora o resultado é sempre 1000. O trecho entre `Lock()` e `Unlock()` é chamado de **seção crítica**: só uma goroutine entra por vez.

## Idiomático: `defer Unlock()`

Para não esquecer de destravar (em um `return` antecipado ou um `panic`, por exemplo), use `defer`:

```go
type Contador struct {
	mu sync.Mutex
	n  int
}

func (c *Contador) Inc() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.n++
}
```

Repare que o mutex fica **dentro da struct**, junto do dado que ele protege. Esse é o padrão comum em Go.

## Pontos de atenção

- **Nunca copie um mutex** depois de usado. Use ponteiros (`*Contador`), como no exemplo acima. O `go vet` avisa sobre isso.
- **Deadlock**: se você dá `Lock()` duas vezes na mesma goroutine sem `Unlock()`, ela trava para sempre.
- **`sync.RWMutex`**: permite vários leitores ao mesmo tempo, mas só um escritor. Útil quando se lê muito mais do que se escreve.
- **Detectar bugs**: rode `go run -race main.go` (ou `go test -race`). O detector de corrida do Go aponta acessos concorrentes sem proteção.

## Mutex ou channel?

Go também tem *channels*, e o lema é "compartilhe memória comunicando, não comunique compartilhando memória". Na prática:

- **Mutex**: para proteger um estado simples compartilhado (contadores, caches, mapas).
- **Channel**: para passar dados ou coordenar o trabalho entre goroutines.

Nenhum é "o certo" sempre. Para um contador ou um mapa, o mutex costuma ser mais simples.

Se quiser, posso mostrar como proteger um `map` (que em Go **não** é seguro para uso concorrente) ou comparar com a versão usando channels.
