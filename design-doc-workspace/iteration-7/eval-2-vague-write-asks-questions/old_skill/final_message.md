O diretório de trabalho está vazio — não há docs de design existentes, template de casa, nem código para eu verificar por conta própria. O prompt é vago, e a skill é explícita: quando os fundamentos faltam, a entrega da rodada são as perguntas, não um esqueleto de seções com placeholder. Não vou criar arquivo nesta rodada.

Minha resposta ao usuário, em português:

---

Posso escrever o design doc, mas do jeito que está o pedido eu teria que inventar o conteúdo que dá valor ao documento — o problema real, os números, os trade-offs. Um design doc registra o raciocínio de vocês, não o meu. Antes de criar o arquivo, preciso que você me responda algumas perguntas:

1. **O que dói no monólito hoje, e por que agora?** Deploy lento? Times pisando uns nos outros? Um componente que não escala? Incidentes? Se tiver números (tempo de build/deploy, frequência de release, tamanho do time), melhor ainda — são eles que sustentam a motivação.

2. **Como vocês vão saber que a migração deu certo — existe um número?** E o que está explicitamente *fora* de escopo desta fase (ex.: reescrever o frontend, trocar de banco, migrar tudo de uma vez)?

3. **Qual é a estratégia e o primeiro passo concreto?** Vocês já pensaram em algo — strangler fig extraindo um domínio por vez, quebrar por contexto de negócio, começar por qual serviço? E o que acontece com o banco de dados compartilhado, que costuma ser a parte mais difícil?

4. **Quais alternativas foram consideradas e por que perderam** — inclusive "não fazer nada" e o meio-termo comum, modularizar o monólito sem distribuí-lo? Se "continuar como está" nem merece refutação, o problema do item 1 provavelmente está mal contado.

5. **Quem fora do time é impactado, e quem deve revisar o documento?** Infra/plataforma (novos deploys, observabilidade, service discovery), segurança (nova superfície de rede), outros times que consomem APIs do monólito — e qual é o custo operacional que vocês aceitam pagar (mais serviços = mais on-call, mais latência de rede, consistência eventual)?

Com essas respostas eu escrevo o documento: cabeçalho, visão geral, contexto, objetivos e fora de escopo, o design (com diagrama de containers C4 e fluxos de sequência das partes migradas), trade-offs da solução escolhida, alternativas consideradas, plano de implantação incremental e questões em aberto. Só me diga também onde salvar — sugiro `docs/design/` se o repositório ainda não tem um lugar para design docs.
