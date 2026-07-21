Não vou escrever ainda — com o que tenho aqui, o ADR sairia inventado.

"Vamos trocar o Redis" me dá metade de uma frase da seção Decision e nada do resto. Um ADR honesto precisa de três coisas: a decisão concreta, as forças que levaram a ela (o que está ruim hoje, e por que agora) e o trade-off que vocês aceitaram. Se eu preencher isso no chute, o próximo dev vai ler um motivo que ninguém nunca teve — e é exatamente isso que estraga um log de decisões.

Me responde essas e eu escrevo na sequência:

1. **Trocar o Redis por o quê, e usado para quê hoje?** (cache, sessão, fila, lock distribuído, pub/sub?) O substituto é outra tecnologia — Valkey, Memcached, Postgres, ElastiCache/Momento, algo em memória no próprio processo — ou é o mesmo Redis em outro modelo de operação (self-hosted → gerenciado, por exemplo)?

2. **Por que agora?** Qual foi a dor concreta que empurrou isso: custo, mudança de licença, limite de memória/latência, esforço de operação, incidente recente, fim de suporte?

3. **O que mais estava na mesa e foi descartado?** Mesmo que a resposta seja "só consideramos uma opção", isso é informação útil pro registro.

4. **Qual o preço que vocês aceitaram pagar?** Migração de dados, perda de algum comando/estrutura que o Redis tem, reescrita de código, período de dual-write, time que precisa aprender a nova coisa. Decisão sem contrapartida é sinal de que a Consequences vai virar folheto de vendas.

E um detalhe rápido: **isso já está fechado ou ainda é proposta?** Isso define se o Status sai como `Accepted` ou `Proposed`.

Uma observação sobre o repositório: não existe log de decisões aqui ainda (nenhum `.adr-dir`, nenhum `doc/adr`). Então, quando você responder, eu crio o log do zero — `doc/adr/` com o ADR inicial "Registrar decisões de arquitetura" (`0001`) e a sua decisão sobre o Redis como `0002`. Se preferir outro diretório, é só falar.
