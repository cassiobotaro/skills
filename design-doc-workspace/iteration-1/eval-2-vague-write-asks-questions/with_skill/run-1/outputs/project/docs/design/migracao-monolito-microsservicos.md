# Migração do monolito para microsserviços

> **Estado deste documento: ESQUELETO / RASCUNHO INICIAL.**
> Este arquivo é um andaime. As seções abaixo estão estruturadas, mas o conteúdo
> de cada uma depende de informações que só você (ou o time) pode fornecer — um
> design doc honesto registra o raciocínio real do autor, ele não inventa
> problemas, metas, métricas nem alternativas. Cada bloco `> ❓` marca exatamente
> o que falta. As perguntas correspondentes estão na minha mensagem; conforme você
> responder, eu preencho as seções.
>
> **Atenção especial:** migrar de monolito para microsserviços é uma das decisões
> em que "manter o monolito" (eventualmente modularizado) costuma ser uma
> alternativa séria. Por isso não vou escrever justificativas a favor da migração
> que você não tenha estabelecido — sem o problema real na mão, qualquer "por que
> microsserviços" seria propaganda, não engenharia.

| | |
|---|---|
| **Documento** | DESIGN-DOC |
| **Estado** | Rascunho |
| **Título** | Migração do monolito para microsserviços |
| **Autores** | _(a definir)_ |
| **Revisores** | _(a definir — sugerir áreas/times impactados)_ |
| **Criado** | 2026-06-07 |
| **Última atualização** | 2026-06-07 |
| **Tags** | migração, arquitetura, microsserviços |

## Visão geral

> ❓ Em uma ou duas frases: qual problema essa migração resolve e que tipo de
> solução ela entrega? (Sem detalhes — só o assunto do documento.)

## Escopo e contexto

> ❓ O que existe hoje? Descreva o monolito atual: linguagem/stack, principais
> módulos ou domínios, banco(s) de dados, volume de tráfego, time(s) que mexem
> nele. E o que está motivando esse trabalho **agora** (o que dói hoje:
> deploys lentos, acoplamento entre times, escalabilidade de uma parte específica,
> incidentes, etc.)? Fatos de fundo apenas — nada de metas nem soluções aqui.

## Objetivos e fora de escopo

> ❓ Como você vai saber que deu certo? De preferência um número
> (ex.: "reduzir o tempo de deploy de X para Y", "permitir que o time de
> pagamentos faça deploy sem coordenar com os outros 4 times", "escalar o serviço
> de busca de forma independente"). E qual problema relacionado você
> **explicitamente não** vai resolver desta vez (ex.: "não vamos quebrar o módulo
> de billing nesta fase", "reescrita de UI fica fora")?

## A solução proposta

> ❓ Quais serviços você pretende extrair primeiro e por quê? Como eles se
> comunicam (HTTP/REST, gRPC, mensageria/eventos)? O que acontece com o banco de
> dados — banco por serviço, banco compartilhado durante a transição, padrão de
> sincronização? Qual decisão dessa solução é a que você está **menos seguro**?
>
> Quando houver substância aqui, esta seção vira uma série de subseções:
> arquitetura (diagrama C4 de containers), fluxos principais (diagramas de
> sequência), contratos de API relevantes e dados sensíveis envolvidos.

## Trade-offs da solução escolhida

> ❓ O que **piora** em troca dos benefícios? Microsserviços cobram um preço real:
> complexidade operacional, latência de rede entre chamadas, consistência
> eventual, observabilidade distribuída, mais superfície de deploy. Qual desses
> custos o time está disposto a aceitar — e tem como bancar (plataforma,
> CI/CD, on-call)?

## Alternativas consideradas

> ❓ O que mais foi considerado? No mínimo:
> - **Não fazer nada / manter o monolito como está** — por que isso não basta?
> - **Modularizar o monolito (monólito modular) sem distribuir** — por que não?
> - Outras opções que vocês discutiram.
>
> O valor de longo prazo do doc está em registrar por que cada alternativa perdeu.

## Concerns transversais

> ❓ Quem fora do seu time é impactado? A migração adiciona carga a algum sistema
> compartilhado, expõe nova superfície de segurança, muda uma API da qual alguém
> depende, ou exige trabalho de infraestrutura/plataforma? Liste os times e
> sugira-os como revisores no cabeçalho.

## Plano de implantação

> ❓ Isso vai em fases? Migração de monolito quase sempre é incremental
> (ex.: padrão strangler fig). Descreva as fases em alto nível e a história de
> rollback se uma fase der errado.

## Questões em aberto

> ❓ O que ainda está indefinido? (ex.: "ownership da plataforma de mensageria",
> "ainda não sabemos se o módulo X pode ser extraído sem reescrever o schema").
