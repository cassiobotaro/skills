O diretório de trabalho está vazio — não há repositório com código, template de design doc, nem docs anteriores para eu extrair contexto. O pedido é genérico demais para preencher as seções com honestidade, então, seguindo o contrato da skill (registrar, não inventar), a entrega desta rodada são as perguntas, não um esqueleto de documento. Nenhum arquivo foi criado.

Minha resposta ao usuário, em português:

---

Posso escrever o design doc, mas do jeito que está o pedido eu teria que inventar o conteúdo que dá valor ao documento — o problema real, os trade-offs e as alternativas — e isso produziria um doc genérico sobre "monolito → microserviços" que não registra o raciocínio do *seu* time. Não encontrei no diretório nenhum código, template ou design doc anterior para extrair esse contexto, então preciso que você me responda algumas perguntas antes de criar o arquivo:

1. **O que dói hoje no monolito, e por que agora?** Deploys lentos ou acoplados demais? Times pisando no código uns dos outros? Um módulo específico que não escala? Custo? A motivação concreta define o problema — e também o critério para saber se a migração valeu a pena.

2. **Qual o objetivo mensurável e o que está fora de escopo?** Por exemplo: "reduzir o lead time de deploy de 2 semanas para 1 dia" é verificável; "ficar mais escalável" não é. E o que vocês deliberadamente *não* vão fazer nessa primeira fase (reescrever o frontend? trocar o banco? migrar tudo de uma vez)?

3. **Qual é a estratégia de decomposição que vocês têm em mente?** Extração incremental (strangler fig) começando por qual domínio/módulo? Big bang? Já existe uma fronteira óbvia (ex.: faturamento, catálogo) candidata a primeiro serviço? E como fica o banco de dados — compartilhado durante a transição ou um por serviço desde o início?

4. **Que alternativas o time considerou e por que foram descartadas?** Em particular: por que *não fazer nada* (ou apenas modularizar melhor o monolito) não resolve? Essa é a comparação que todo revisor vai fazer, e o doc precisa respondê-la com os argumentos de vocês.

5. **Quem fora do time é impactado, e quais são as restrições?** Outros times que consomem APIs do monolito, infraestrutura (vocês já operam Kubernetes/containers ou isso é novo?), segurança, compatibilidade com integrações existentes, prazo ou orçamento que limite as opções.

Com essas respostas eu escrevo o documento — com o problema, os objetivos, a solução proposta, os trade-offs aceitos e as alternativas descartadas, mais um diagrama de containers (C4) da arquitetura-alvo e o plano de implantação incremental. Também me diga onde você quer salvar o doc (sugiro `docs/design/`) e quem são os autores e revisores.
