Não há log nem menção a Redis no repositório, e o pedido não diz o que substitui o Redis nem por quê. Preciso de algumas respostas antes de escrever, para não inventar o motivo.

1. **Substituir por quê?** Qual é o substituto (Memcached, Valkey, Postgres, outro)?
2. **Por que agora?** Qual problema com o Redis motivou a troca (custo, licença, operação, desempenho, outro)?
3. **Alternativas:** o que mais foi considerado e descartado?
4. **O que se abre mão ou se aceita em troca?** Por exemplo, uma funcionalidade que o Redis dava, o custo da migração ou um risco.
5. **Status:** a decisão já está fechada (`Accepted`) ou ainda aguarda concordância (`Proposed`)?

Também não existe log de ADRs neste repositório. Vou criar `doc/adr/` com o ADR 0001 padrão ("Registrar decisões de arquitetura"), traduzido para português. A decisão do Redis será o 0002. Se você preferir outro diretório, me diga.
