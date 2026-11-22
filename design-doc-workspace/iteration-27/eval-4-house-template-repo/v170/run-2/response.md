Passei o `technical-writing` e o `unslop` no texto. O `unslop` não achou nada para cortar, então só o `technical-writing` gerou edições (nomeei quem mede a carga do Redis e quem recebe o alerta). Não tem travessão no texto.

Criei `docs/design/dd-2026-008-rate-limiting-api-publica.md`.

Segui o padrão do DD-2026-007, o único doc que existe em `docs/design/`: cabeçalho em tabela, Resumo, Contexto, Proposta com Compensações ✓/✗, Riscos em tabela e Plano de entrega. Continuei a numeração com DD-2026-008.

**Onde fugi do padrão:**
- Acrescentei **Objetivos** e **Alternativas consideradas**, porque o padrão não tem lugar para eles. Pus "não fazer nada" entre as alternativas, com o INC-4412 como motivo.
- Acrescentei **Perguntas em aberto**, para o que você não me deu.

Se preferir manter o esqueleto idêntico ao DD-007, me diga e eu incorporo essas seções dentro de Contexto e Proposta.

**Decisões minhas que você deve conferir:**
- **Autores:** pus `cassiobotaro`, o usuário do git. Troque se for outra pessoa.
- **Revisores:** deixei "A definir" e listei como pergunta em aberto.
- **Estado:** Rascunho.
- **Data do incidente:** escrevi 2026-11-21, a partir do seu "ontem".
- **NAT:** não virou risco. Registrei na Proposta que o limite é por token, então NAT compartilhado não afeta o desenho.

**Perguntas em aberto no doc, que só você ou o time respondem:**
1. Quem revisa (Plataforma, SRE, Contas)?
2. Se o Redis cair, o gateway deixa passar ou bloqueia?
3. Como o gateway liga cada token ao plano e ao limite negociado dos enterprise?
4. O que acontece com requisição sem token válido?
5. Quanto dura cada fase do plano de entrega, e qual critério libera a próxima?

Não incluí uma seção de "fora de escopo" porque você não citou nada. Se houver algo que alguém poderia esperar que o doc cobrisse, me conte e eu acrescento.
