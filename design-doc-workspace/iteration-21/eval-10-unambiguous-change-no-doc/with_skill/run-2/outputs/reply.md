Ainda não criei o arquivo em `docs/design/`. Do jeito que você descreveu, não vejo nada em aberto: uma coluna nova nullable em `clientes`, um campo opcional no formulário e o mesmo campo no `PUT /clientes/{id}`. Sem escolha a fazer, o documento viraria um manual de implementação, e o code review já cobre isso. Inventar alternativas e riscos só para encher o texto não ajudaria ninguém.

Uma pergunta antes de eu escrever:

- Existe alguma decisão realmente em aberto nessa mudança? Alguns exemplos: validação e formato do telefone (E.164, só dígitos ou texto livre), mascaramento por ser dado pessoal (LGPD), como a migração roda em produção na tabela `clientes`, ou clientes de API que dependem do contrato atual do `PUT`.
- Ou o processo do seu time exige um design doc mesmo para uma mudança assim? Nesse caso eu escrevo um mini-doc enxuto em `docs/design/`, só com o que você me confirmar. Não vou criar alternativas nem riscos que você não tenha estabelecido.

Se for o primeiro caso, me conte a decisão e as opções que vocês pesaram, e eu escrevo o documento em torno delas.
