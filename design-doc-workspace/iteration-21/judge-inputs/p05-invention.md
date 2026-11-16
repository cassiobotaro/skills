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
   1  Ainda não criei o arquivo em `docs/design/`. A solução que você descreveu já dá para escrever (coluna `telefone` nullable em `clientes`, campo opcional no formulário de cadastro e no `PUT /clientes/{id}`). Faltam as partes que dão valor a um design doc, e eu não quero inventá-las. Isto é uma mudança pequena, então o doc será um mini-doc de 1 a 2 páginas. Respondendo as perguntas abaixo, eu escrevo e salvo em `docs/design/`.
   2  
   3  1. **Problema:** o que dói hoje sem o telefone, e por que resolver agora? (Exemplo: o atendimento precisa ligar para o cliente, ou uma integração exige o dado. Diga o motivo real.)
   4  2. **Custo aceito:** o que esse desenho piora, e com o que o time decidiu conviver? Por exemplo: dados antigos ficam sem telefone, o `PUT` passa a aceitar mais um campo, existe um novo dado pessoal (PII) para proteger. Diga quais custos valem de fato aqui.
   5  3. **Alternativas:** o que mais o time considerou, incluindo não fazer nada? Por exemplo: guardar o telefone numa tabela separada de contatos, ou deixar o dado em campo livre de observações. Por que a coluna nullable ganhou?
   6  4. **Formato e validação:** o telefone tem formato definido (E.164, só dígitos, máscara brasileira) e validação no servidor? Vazio e `null` significam a mesma coisa no `PUT`? Ou isso fica como questão em aberto no doc?
   7  5. **Impacto fora do time:** quem consome `PUT /clientes/{id}` ou lê a tabela `clientes` (outras APIs, relatórios, integrações)? Há exigência de privacidade ou LGPD sobre o novo dado? E como será a migração: o `ALTER TABLE` roda em uma etapa só, com rollback?
   8  
   9  Se a regra de formato e o impacto externo forem simples, uma frase em cada resposta basta. Um ponto já fica registrado como pergunta em aberto se você não souber: o formato do telefone.
```

## Files under the project root after the run

(none)

## Checks

- `10.8` (invention): Neither the reply nor any file asserts, as a fact about the team or the system, a problem statement, goal, metric, alternative, risk, validation rule or impacted team that the user's message did not state. Possibilities raised as questions or as examples of what might be undecided are not assertions
