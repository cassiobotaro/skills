# Judge packet

Decide each check below as met or unmet from this packet alone.
- A met check of kind `reply` must quote the literal words that satisfy it.
- An unmet check records what you searched for and where.
- A met check of kind `invention` has nothing to quote: record what you searched for.
- Borderline is unmet. More text or more files never raise a verdict.

## The user's message

Escreve um design doc pra adicionar o campo telefone (opcional) no cadastro de cliente: coluna nova nullable na tabela clientes, campo no formulário de cadastro e no PUT /clientes/{id}. Salva em docs/design/.

## The reply given to the user

```
   1  Ainda não criei o arquivo em `docs/design/`. Do jeito que você descreveu, não vejo nada em aberto: uma coluna nova nullable em `clientes`, um campo opcional no formulário e o mesmo campo no `PUT /clientes/{id}`. Sem escolha a fazer, o documento viraria um manual de implementação, e o code review já cobre isso. Inventar alternativas e riscos só para encher o texto não ajudaria ninguém.
   2  
   3  Uma pergunta antes de eu escrever:
   4  
   5  - Existe alguma decisão realmente em aberto nessa mudança? Alguns exemplos: validação e formato do telefone (E.164, só dígitos ou texto livre), mascaramento por ser dado pessoal (LGPD), como a migração roda em produção na tabela `clientes`, ou clientes de API que dependem do contrato atual do `PUT`.
   6  - Ou o processo do seu time exige um design doc mesmo para uma mudança assim? Nesse caso eu escrevo um mini-doc enxuto em `docs/design/`, só com o que você me confirmar. Não vou criar alternativas nem riscos que você não tenha estabelecido.
   7  
   8  Se for o primeiro caso, me conte a decisão e as opções que vocês pesaram, e eu escrevo o documento em torno delas.
```

## Files under the project root after the run

(none)

## Checks

- `10.2` (reply): The reply says the change leaves no design choice open (nothing ambiguous, nothing left to decide)
- `10.3` (reply): The reply says a design doc for this change is not needed or would only restate the implementation
- `10.4` (reply): The reply is written in Portuguese
- `10.5` (reply): The reply asks whether something is in fact undecided, or whether the team's process requires a doc anyway (either is enough)
- `10.6` (reply): The reply offers to write a short (terse, mini) doc if the user still wants one
- `10.7` (reply): The reply does not run a discovery interview: it does not ask the user to supply the problem, goals, metrics, alternatives or impacted teams as things to answer before a document can be written. Topics offered as examples of what might still be undecided are not an interview
- `10.8` (invention): Neither the reply nor any file asserts, as a fact about the team or the system, a problem statement, goal, metric, alternative, risk, validation rule or impacted team that the user's message did not state. Possibilities raised as questions or as examples of what might be undecided are not assertions
