Revisei o `docs/design/fanout-de-notificacoes.md`. O documento descreve bem *o que* será construído, mas hoje ele não registra *por que* — não há nenhum custo, nenhuma alternativa e nenhum número. Isso é o achado principal: do jeito que está, o doc perde o valor no dia em que o código existir.

Separei em duas partes: o que depende de você e o que eu já apliquei.

## 1. Perguntas para você

**Sobre a régua da revisão**

1. O time tem um template de design doc (wiki, drive, Confluence)? O repositório só tem este documento, então usei o catálogo padrão como referência — as sugestões de estrutura abaixo são sugestões, não exigências. Se existir um template oficial, me aponta que eu reavalio a estrutura contra ele.

**Trade-offs e alternativas (o mais importante)**

2. A solução não tem nenhum custo declarado. O que o fanout com filas piorou, encareceu ou tornou mais arriscado, e com o que o time decidiu conviver? Essa é a seção que dá valor de longo prazo ao doc.
3. Que outras opções foram avaliadas antes de escolher o fanout — e por que "não fazer nada" (continuar com o cron, eventualmente ajustado) não é aceitável?
4. Existe algum dado por trás da escolha (medição de latência atual, teste de carga, protótipo)? Sem isso, "melhor performance" fica sem sustentação.

**Objetivos e escopo**

5. Os três objetivos não são verificáveis como estão ("melhorar a performance", "tornar escalável", "garantir o SLA"). Qual é o SLA em números, qual é a latência/volume de hoje e qual é a meta? Com um número, dá para saber depois se o projeto funcionou.
6. Os dois itens de "Fora de escopo" apenas negam os objetivos ("não deve ser lento", "não deve perder notificações") — eles não excluem nada. O que alguém poderia razoavelmente esperar deste trabalho e que ficou de fora de propósito (novos canais, retentativa/política de erro com os providers, migração do histórico, redesenho de templates)?

**Solução e diagrama**

7. No diagrama, push e e-mail têm DLQ, mas in-app não. É proposital ou é um esquecimento?
8. O controle de TPS por provider aparece no texto mas não tem lugar no desenho: ele vive dentro do worker ou é um componente à parte? Não desenhei porque o documento não diz.
9. Os providers e a tabela `notifications` continuam existindo no modelo novo? Se sim, valeria colocá-los no diagrama — não incluí porque o texto atual não os descreve no fluxo proposto.
10. O CDC lê a base de quem? Saber a origem dos eventos de domínio muda quem precisa revisar isto.

**Seções que faltam**

11. **Preocupações transversais** — quem fora do time de mensageria é impactado (infra/DBA por causa do CDC, segurança, times donos dos eventos de domínio, os próprios providers)? Deixei de fora porque não posso adivinhar.
12. **Testabilidade e observabilidade** — como vocês verificam isso antes de subir e o que avisa que quebrou em produção (alarme de profundidade de fila, mensagens na DLQ, latência de entrega ponta a ponta)?
13. **Plano** — o plano tem os passos, mas não tem plano de rollback nem prazos. O cron e o fanout convivem durante a migração do e-mail? O que acontece se a etapa 2 der errado?
14. **Perguntas em aberto** — tem algo ainda indefinido ou dependendo de outro time?

**Cabeçalho**

15. O estado está "Em revisão" desde 10/02 e hoje é 07/08. Ainda está em revisão, ou já foi aprovado/implementado? E quem são os revisores nomeados, com suas áreas?

Não preenchi nenhuma dessas seções com texto de exemplo — seção vazia com boilerplate é pior que seção ausente. Elas entram no documento assim que você responder.

## 2. Melhorias que já apliquei

- **Glossário no início do documento**, cobrindo os termos que o texto usa sem definir: CDC, DLQ, exchange, fanout, in-app, provider, SLA e TPS. Quem vem de outro time tropeçava em todos.
- **Visão geral enxugada para um parágrafo sem detalhes.** Ela concentrava cron, tabela, DLQ, TPS e CDC logo na abertura — detalhe demais para quem só quer saber do que o doc trata.
- **Nova seção "Escopo e contexto"** com os fatos do modelo atual que estavam presos na visão geral (cron a cada minuto, leitura da tabela `notifications`, montagem de payload por canal, chamada sequencial aos providers). São fatos de contexto, e é onde o leitor espera encontrá-los.
- **Removi a frase de venda** "A solução proposta é mais escalável e robusta que o modelo atual, além de mais fácil de manter". São três adjetivos sem dado por trás, exatamente o tipo de justificativa que não sobrevive ao "por quê?" de um revisor. O ganho volta ao documento em forma de trade-off quando você responder as perguntas 2 a 4.
- **Diagrama de arquitetura reescrito como Structurizr DSL** (visão de contêineres do C4), embutido como referência de imagem com a fonte dobrada num bloco `<details>`, no lugar do flowchart Mermaid. O diagrama passa a dizer o que cada caixa é e o que corre em cada seta. Mantive **só o que o seu texto já dizia**: nenhuma tecnologia foi atribuída — não nomeei broker, banco nem protocolo, porque o documento não nomeia. Mantive também a ausência da DLQ de in-app, em vez de "consertar" no desenho (é a pergunta 7).
- **Prosa explicativa depois do diagrama**, nomeando os componentes e como eles se relacionam. Um diagrama sem texto obriga o leitor a adivinhar o que as caixas significam.
- **Data de última atualização** ajustada para 2026-08-07.

Uma observação sobre o diagrama: não consegui renderizar nem validar o DSL neste ambiente (não há Docker, Structurizr CLI nem MCP disponível), então a linha `![…](diagrams/fanout-de-notificacoes.svg)` está marcando o lugar da imagem para a passada manual. Para gerar e validar:

```
docker run --rm -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl
docker run --rm -v "$PWD":/usr/local/structurizr structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```

Me responde o que quiser das perguntas — mesmo que seja só as de trade-off e alternativas — que eu incorporo ao documento.
