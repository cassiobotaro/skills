Ainda não dá para escrever o ADR. O repositório está vazio, sem código, sem log de ADRs e sem nenhuma menção ao Redis. Qualquer coisa que eu escrevesse sobre o porquê ou sobre o substituto seria inventada, e isso estraga o registro.

Me conta:

1. **Por quem vamos trocar o Redis?** Pode ser Memcached, Valkey, Postgres, outra coisa.
2. **Por que trocar, e por que agora?** Pode ser custo, licença, operação, limitação técnica ou outro motivo. O que incomoda hoje?
3. **Que alternativas vocês avaliaram?** E o que ficou de fora?
4. **Qual desvantagem vocês aceitaram?** Por exemplo, esforço de migração, perder alguma feature ou risco na transição.
5. **A decisão já está fechada ou ainda falta alguém concordar?** Se já está fechada, o status é `Accepted`. Se ainda falta alguém, é `Proposed`.

Também preciso saber onde o Redis foi decidido antes. Se já existe um ADR sobre isso, ele não está neste repositório. Nesse caso, me passa o número e o título, e eu escrevo o novo ADR marcando o antigo como superseded.

Como não há log, vou criar `doc/adr/` com o ADR 0001 padrão ("Record architecture decisions"). A decisão de trocar o Redis vira o `0002`. Se você preferir outro diretório, me avisa.

Com essas respostas eu escrevo o ADR em português. Os títulos de seção e o status ficam em inglês, para o adr-tools conseguir ler.
