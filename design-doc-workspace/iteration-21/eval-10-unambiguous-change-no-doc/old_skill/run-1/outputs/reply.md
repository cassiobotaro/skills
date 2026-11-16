Ainda não criei o arquivo em `docs/design/`. A solução que você descreveu já dá para escrever (coluna `telefone` nullable em `clientes`, campo opcional no formulário de cadastro e no `PUT /clientes/{id}`). Faltam as partes que dão valor a um design doc, e eu não quero inventá-las. Isto é uma mudança pequena, então o doc será um mini-doc de 1 a 2 páginas. Respondendo as perguntas abaixo, eu escrevo e salvo em `docs/design/`.

1. **Problema:** o que dói hoje sem o telefone, e por que resolver agora? (Exemplo: o atendimento precisa ligar para o cliente, ou uma integração exige o dado. Diga o motivo real.)
2. **Custo aceito:** o que esse desenho piora, e com o que o time decidiu conviver? Por exemplo: dados antigos ficam sem telefone, o `PUT` passa a aceitar mais um campo, existe um novo dado pessoal (PII) para proteger. Diga quais custos valem de fato aqui.
3. **Alternativas:** o que mais o time considerou, incluindo não fazer nada? Por exemplo: guardar o telefone numa tabela separada de contatos, ou deixar o dado em campo livre de observações. Por que a coluna nullable ganhou?
4. **Formato e validação:** o telefone tem formato definido (E.164, só dígitos, máscara brasileira) e validação no servidor? Vazio e `null` significam a mesma coisa no `PUT`? Ou isso fica como questão em aberto no doc?
5. **Impacto fora do time:** quem consome `PUT /clientes/{id}` ou lê a tabela `clientes` (outras APIs, relatórios, integrações)? Há exigência de privacidade ou LGPD sobre o novo dado? E como será a migração: o `ALTER TABLE` roda em uma etapa só, com rollback?

Se a regra de formato e o impacto externo forem simples, uma frase em cada resposta basta. Um ponto já fica registrado como pergunta em aberto se você não souber: o formato do telefone.
