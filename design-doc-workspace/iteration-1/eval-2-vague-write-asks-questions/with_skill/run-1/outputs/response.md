Topa, mas preciso de mais substância antes de escrever de verdade.

Um design doc vale justamente pelos **trade-offs** que ele registra — o raciocínio real de quem vai construir o sistema. Se eu escrever um doc completo de migração só com a frase "monolito → microsserviços", vou ter que inventar o problema, as metas, a arquitetura atual e as alternativas — e aí vira propaganda, não engenharia. Isso é especialmente perigoso aqui: "manter o monolito" (ou modularizá-lo sem distribuir) costuma ser uma alternativa séria, e eu não vou escrever justificativas a favor de microsserviços que você não tenha estabelecido.

O repositório está vazio, então também não tenho como descobrir o estado atual sozinho. Por isso fiz o que dá pra fazer honestamente: criei um **esqueleto** do documento em `docs/design/migracao-monolito-microsservicos.md`, com a estrutura toda pronta e cada seção marcando exatamente o que falta. Conforme você responder as perguntas abaixo, eu preencho.

As perguntas que destravam o doc:

1. **O problema (o que dói hoje):** o que está ruim no monolito agora que motiva mexer? Deploys lentos/arriscados, times se atropelando, uma parte específica que não escala, incidentes recorrentes? Seja concreto.

2. **O que existe hoje:** stack/linguagem do monolito, principais módulos ou domínios, banco(s) de dados, volume aproximado de tráfego e quantos times mexem nele.

3. **Como saber que deu certo (de preferência um número):** ex. "reduzir tempo de deploy de X pra Y", "time de pagamentos faz deploy sem coordenar com os outros", "escalar a busca de forma independente". E o que fica **explicitamente fora** desta etapa.

4. **A solução que você tem em mente:** quais serviços extrair primeiro e por quê? Comunicação entre eles (REST, gRPC, eventos/mensageria)? O que acontece com o banco — um por serviço, compartilhado na transição? E qual decisão você está **menos seguro**?

5. **Quem é impactado fora do time** (segurança, plataforma/infra, times que consomem APIs do monolito) — pra eu sugerir como revisores.

Bônus, se já tiver: autores/revisores pro cabeçalho e se você prefere salvar o doc em outro lugar (deixei em `docs/design/` por padrão).

Pode responder em texto corrido mesmo, do jeito que vier — eu organizo. E se em algum ponto a conclusão for "na real, o monolito modular resolve", o doc também serve pra registrar isso.
