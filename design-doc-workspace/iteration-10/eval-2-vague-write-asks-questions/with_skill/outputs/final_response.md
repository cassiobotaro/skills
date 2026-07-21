Posso escrever, mas ainda não com honestidade: uma migração de monolito para microserviços é uma das decisões mais caras que um time toma, e o valor do design doc está justamente em registrar *por que* vocês estão fazendo isso e *o que* aceitaram pagar em troca. Nada disso eu posso inventar — o documento é o seu raciocínio, escrito por mim. Olhei o repositório e ele está vazio: não há docs de design existentes nem template de casa para eu seguir.

Então antes de criar o arquivo, cinco perguntas. Com as respostas eu escrevo o documento inteiro na sequência.

1. **O problema.** O que dói hoje no monolito, concretamente, e por que resolver agora? (Deploys travados por acoplamento entre times? Um ponto do sistema que não escala? Tempo de build? Onboarding?) Se der, um fato ou número que sustente a dor — "o deploy leva 40 min e qualquer time pode quebrá-lo" vale mais do que "está difícil de manter".

2. **As fronteiras.** Como vocês vão saber que a migração deu certo — existe um número (frequência de deploy, lead time, p99 de algum endpoint, custo)? E o que está explicitamente **fora** de escopo desta rodada (por exemplo: o banco continua único? o frontend não muda? algum módulo legado fica onde está?).

3. **A solução.** Qual é o recorte que vocês já têm em mente — quais serviços saem primeiro do monolito e por quê esses? Como eles se comunicam (HTTP síncrono, mensageria, eventos)? E o que acontece com os dados: cada serviço com seu banco, banco compartilhado por enquanto, ou migração de dados por fases?

4. **As alternativas.** O que mais foi considerado e por que perdeu? Em especial: por que **não fazer nada** (ou só continuar melhorando o monolito) não é aceitável, e vocês avaliaram um **monolito modular** — separar módulos e limites internos sem separar processos? Se essa opção foi descartada, o motivo é a parte mais importante do documento.

5. **O raio de impacto.** Quem fora do seu time é afetado — infraestrutura (novos serviços, service mesh, observabilidade), segurança (novas superfícies de rede, autenticação entre serviços), times que consomem APIs do monolito hoje, carga adicional em sistemas compartilhados? E quem deveria revisar o documento por cada uma dessas áreas?

Duas coisas menores, se você já souber: vocês têm um **template de design doc** (wiki, drive, um doc antigo) que eu deva seguir? Se tiver, ele manda nas seções e eu pergunto o que faltar para preencher cada uma. E onde salvo o arquivo — sugiro `docs/design/migracao-monolito-microservicos.md`, mas se o time já guarda em outro lugar, me diga.

Se preferir, responda só o que estiver claro hoje: o que ficar em aberto eu registro numa seção de **Questões em aberto** no documento, em vez de preencher com suposição.
