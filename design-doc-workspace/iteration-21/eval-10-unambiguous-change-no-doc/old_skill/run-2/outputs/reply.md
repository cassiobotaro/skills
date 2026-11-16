Antes de salvar o doc em `docs/design/`, preciso de algumas respostas. Você me deu a solução (coluna nullable, campo no formulário, campo no `PUT /clientes/{id}`), mas não deu o problema, o custo aceito nem as alternativas. Se eu escrevesse agora, teria que inventar essas partes. O repositório está vazio, então também não encontrei nada que eu possa verificar sozinho.

1. **Problema:** o que dói hoje sem o telefone no cadastro, e por que isso entra agora? Quem vai usar o dado (atendimento, cobrança, notificações)?
2. **Custos aceitos:** o que essa abordagem piora ou deixa em aberto? Por exemplo: validação e formato do número (só dígitos, DDI, máscara?), dado pessoal novo (LGPD), clientes antigos ficando sem telefone, clientes de API que mandam `PUT` sem o campo (apagam o valor ou o preservam?).
3. **Alternativas:** o que o time considerou além da coluna nova em `clientes`? Por exemplo: tabela separada de contatos, ou não fazer nada. Por que a coluna nullable ganhou?
4. **Quem é afetado fora do time:** outros sistemas leem `clientes` ou consomem o `PUT /clientes/{id}` (BI, integrações, front-end de outro time)? Há quem deva revisar (segurança, DBA)?
5. **Entrega:** a migração e o deploy acontecem de uma vez, ou em etapas, com plano de rollback?

Também confirme os autores e revisores para o cabeçalho.

Com essas respostas eu escrevo o doc, em português, em `docs/design/` (por exemplo `docs/design/telefone-no-cadastro-de-cliente.md`). Por ser uma mudança pequena, ele deve ficar com 1 a 3 páginas.
