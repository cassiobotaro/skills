Pronto. Escrevi a decisão como ADR em `doc/adr/0002-gerar-pdfs-de-fatura-em-background-via-sidekiq.md`, com o status `Accepted`.

Como não existia log de decisões no repositório, também criei o `doc/adr/0001-registrar-decisoes-de-arquitetura.md`, a seed padrão do adr-tools, traduzida para português. Se o time já tiver um log em outro lugar, me avise que eu ajusto.

O ADR registra o que foi decidido na sync: gerar o PDF em background no Sidekiq existente, gravar no bucket de documentos e mandar um e-mail com o link. Também registra as alternativas descartadas (timeout de 120s e API de PDF de terceiros) e as consequências que o time aceitou: o download imediato some até para faturas pequenas, e a fila compartilhada com o time de e-mail pode sentir a carga.

Uma coisa que deixei de fora de propósito: a renomeação do módulo de billing não é uma decisão tomada, então não virou ADR. Se quiserem registrar, precisa ser uma decisão com motivo e alvo definidos.
