Um **mutex** (de *mutual exclusion*, exclusão mútua) é uma trava que garante que só uma goroutine por vez execute um trecho de código.

## Por que você precisa disso

No JavaScript você quase nunca pensa nisso, porque o código roda numa única thread com event loop. Entre um `await` e outro, ninguém mexe nas suas variáveis.

Em Go, goroutines rodam de verdade em paralelo, em várias threads do sistema. Se duas delas mexem na mesma variável ao mesmo tempo, você tem uma **race condition**:

```go
var contador int

func main() {
    var wg sync.WaitGroup
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            contador++ // PERIGO: não é atômico
        }()
    }
    wg.Wait()
    fmt.Println(contador) // quase nunca dá 1000
}
```

`contador++` parece uma operação só, mas são três: ler, somar, escrever. Duas goroutines podem ler o mesmo valor e uma sobrescreve o resultado da outra.

## A solução: `sync.Mutex`

```go
var (
    contador int
    mu       sync.Mutex
)

func main() {
    var wg sync.WaitGroup
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            mu.Lock()         // só passa quem pegar a trava
            contador++
            mu.Unlock()       // libera para a próxima
        }()
    }
    wg.Wait()
    fmt.Println(contador) // sempre 1000
}
```

Pense numa porta de banheiro com chave: quem pega a chave (`Lock`) entra, os outros esperam na fila, e quando a pessoa sai e devolve a chave (`Unlock`), o próximo entra.

## Boas práticas

- **Use `defer mu.Unlock()`** logo após o `Lock()`. Assim a trava é liberada mesmo se a função der `return` cedo ou panicar:
  ```go
  mu.Lock()
  defer mu.Unlock()
  ```
- **Mantenha a seção crítica pequena.** Quanto mais tempo você segura a trava, mais as outras goroutines ficam esperando.
- **Agrupe o mutex com o dado que ele protege**, numa struct:
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
- **Nunca copie um mutex** depois de usá-lo. Passe a struct por ponteiro.
- **Não faça `Lock` duas vezes na mesma goroutine** sem `Unlock` no meio: isso trava o programa (deadlock).
- Se há muita leitura e pouca escrita, existe o `sync.RWMutex`, que permite várias leituras simultâneas.

## Dica para quem vem do JS

Go tem um lema: *"Não comunique compartilhando memória; compartilhe memória comunicando."* Em muitos casos, em vez de mutex, dá para usar **channels**. Mas para proteger um estado simples, como um contador ou um cache, o mutex é mais direto e perfeitamente idiomático.

Para detectar race conditions, rode seu código com `go run -race main.go` ou `go test -race`.
