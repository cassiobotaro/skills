**Um mutex é um cadeado que garante que só uma goroutine por vez mexa em um dado compartilhado.** O nome vem de *mutual exclusion* (exclusão mútua).

Estou assumindo que você conhece JavaScript, mas ainda não viu goroutines. Se já conhece, me diga e eu pulo essa parte.

**Por que isso não existe no JS do dia a dia**

O JS roda seu código em uma thread só. Uma função não é interrompida no meio por outra, então dois trechos de código nunca mexem na mesma variável ao mesmo tempo.

Em Go, goroutines podem rodar de verdade em paralelo, em vários núcleos. Aí aparece um problema novo:

```go
var contador int

func main() {
    var wg sync.WaitGroup
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            contador++ // parece uma operação só, mas não é
        }()
    }
    wg.Wait()
    fmt.Println(contador) // esperado: 1000. Real: muitas vezes menos
}
```

`contador++` são três passos: ler o valor, somar 1 e gravar. Suponha que duas goroutines leiam `41` ao mesmo tempo. As duas gravam `42`, e um incremento se perde. Isso se chama *data race*, e o resultado muda a cada execução.

**A correção com mutex**

```go
var (
    mu       sync.Mutex
    contador int
)

go func() {
    defer wg.Done()
    mu.Lock()   // se outra goroutine já tem o cadeado, espera aqui
    contador++
    mu.Unlock() // libera para a próxima
}()
```

Só quem passou por `Lock()` executa o trecho até o `Unlock()`. As outras ficam esperando na fila. Agora o resultado é sempre 1000.

**Uma analogia, com limite**

Pense num banheiro com uma chave: quem pega a chave entra e os outros esperam. A chave é o mutex, o banheiro é o trecho protegido (a *seção crítica*) e esperar na porta é o `Lock()` bloqueando. A analogia falha em um ponto: o mutex não protege a variável em si. Ele só funciona se todo o código que acessa `contador` pegar o cadeado. Se um único lugar esquecer, a proteção some e o compilador não avisa.

**Na prática, em Go**

- Use `defer mu.Unlock()` logo depois do `Lock()`. Assim você não esquece de liberar, mesmo se a função retornar cedo ou der `panic`.
- O mutex costuma ficar dentro de uma struct, ao lado do dado que protege.
- Para achar races, rode `go run -race` ou `go test -race`. Isso é uma ferramenta que conheço bem, mas confira na documentação a saída exata na sua versão.
- Este é o resumo para começar. Existem também `sync.RWMutex`, `sync/atomic` e canais, que resolvem problemas parecidos de outras formas. Você vai precisar deles quando o caso real for mais complexo que um contador.

**Uma pergunta para testar se ficou claro:** se duas goroutines só *leem* a mesma variável e nenhuma escreve, você precisa de mutex? E se uma lê e a outra escreve?
