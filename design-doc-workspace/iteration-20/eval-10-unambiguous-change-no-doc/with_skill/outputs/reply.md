Não escrevi o design doc ainda, porque do jeito que você descreveu não sobra nenhuma escolha em aberto: coluna `telefone` nullable em `clientes`, campo opcional no formulário e no `PUT /clientes/{id}`. Um documento sobre isso só conseguiria repetir o que o diff vai mostrar, e o code review já cobre esse papel. Para preencher seções como alternativas ou riscos eu teria que inventar conteúdo.

Antes de eu seguir, uma pergunta só: tem algo aqui que ainda não está decidido, ou o processo do time exige um doc mesmo assim?

Exemplos do que tornaria o doc útil, se algum deles ainda estiver em discussão:

- formato e validação do telefone (texto livre ou normalizado, só nacional ou com DDI);
- tratamento do telefone como dado pessoal (LGPD, mascaramento, quem pode ler);
- impacto em outros consumidores da tabela `clientes` ou do contrato da API;
- como aplicar a migração em produção.

Se algum desses pontos estiver aberto, me conta o que o time já pensou e eu escrevo o doc em torno dessa decisão. Se for só exigência de processo, me avisa que eu salvo um mini-doc enxuto em `docs/design/`, registrando apenas o que você já definiu, sem alternativas nem riscos fabricados.

Nada foi criado em `docs/design/` por enquanto.
