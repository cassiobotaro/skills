Ainda não criei o arquivo em `docs/design/`, porque pelo que você descreveu não vejo nenhuma decisão em aberto para o doc registrar.

Uma coluna nullable nova em `clientes`, um campo no formulário de cadastro e o mesmo campo no `PUT /clientes/{id}` já definem a solução inteira. Um design doc existe para registrar escolhas e trade-offs. Aqui ele viraria um manual de implementação, e o code review já cobre isso. Inventar alternativas e riscos só para encorpar o documento seria o pior resultado.

Uma pergunta, para eu seguir no caminho certo:

- Existe algo ainda indefinido neste desenho? Alguns exemplos: o formato e a validação do telefone (E.164, só números, com DDI), unicidade ou uso do telefone em outro fluxo (notificação, busca, deduplicação), impacto em outros consumidores da API ou em integrações, backfill ou migração dos clientes existentes, ou privacidade e LGPD do dado novo.
- Ou o doc é exigência do processo do time, mesmo sem nada em aberto? Se for, escrevo um mini-doc curto e direto em `docs/design/`, sem alternativas ou riscos inventados.

Se for um dos exemplos acima, me conte o que a equipe já decidiu e o que ainda está em discussão. Com isso eu escrevo o doc em torno dessa escolha, com os trade-offs.
