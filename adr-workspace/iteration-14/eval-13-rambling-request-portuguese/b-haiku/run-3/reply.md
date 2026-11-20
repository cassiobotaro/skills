Escrevi o ADR da decisão de mover a geração do PDF de fatura para um job em background no Sidekiq.

Como o repositório não tinha log de decisões, criei `doc/adr/` com o seed padrão "Registrar decisões de arquitetura" como `0001`, e este ADR ficou como `0002`. Se o log real já existe em outro lugar, me diga o caminho e eu movo os arquivos para lá.

Duas coisas que deixei de fora do ADR, de propósito:

- A renomeação do módulo de billing não é uma decisão tomada ainda, então não há o que registrar. Se o time decidir, vira um ADR próprio.
- O ADR não inclui números de tempo de geração nem de volume da fila, porque não os recebi. Se tiverem essas medições, dá para acrescentar no Context.

Uma pergunta: o ADR está como `Accepted`, porque a decisão foi fechada na sync de quinta. Se ainda houver alguém que não concordou, me avise para eu marcar como `Proposed`.
