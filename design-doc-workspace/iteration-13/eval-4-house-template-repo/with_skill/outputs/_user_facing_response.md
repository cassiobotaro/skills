Li o `docs/design/dd-2026-007-cache-de-catalogo.md` e segui o padrão da casa: tabela de cabeçalho, **Resumo → Contexto → Proposta (com `### Compensações`) → Riscos (tabela) → Plano de entrega**, numeração `DD-2026-NNN` e nome de arquivo em slug.

Doc novo: **`docs/design/dd-2026-008-rate-limiting-da-api-publica.md`**

## Onde saí do padrão (e por quê)

Você me deu duas coisas que o padrão do DD-2026-007 não tem onde guardar, e preferi acrescentar seção a jogar fora o que você disse. As duas ficaram na ordem natural do esqueleto da casa, que continua intacto:

- **`## Objetivos`** (depois do Contexto) — o "nenhum token excede seu limite por mais de 1s" e o "aguentar um cliente abusivo sem degradar os demais" são metas verificáveis; enterradas no Resumo elas não servem de critério de aceite.
- **`## Alternativas consideradas`** (depois da Proposta) — limitar dentro de cada serviço e o módulo pago do gateway gerenciado, cada uma com o motivo do descarte. É a parte que dá valor ao doc daqui a um ano; sem ela ninguém sabe por que o rate limit não ficou no serviço.

Se vocês preferirem manter o padrão estrito, eu dobro as duas para dentro de Resumo/Proposta — mas a recomendação é deixar como está, e talvez adotar essas duas seções no padrão.

Duas outras decisões que valem seu olhar:

- **Deixei o falso positivo com NAT compartilhado de fora.** Você mesmo concluiu que ele não existe, já que a chave de contagem é o token e não o IP. Registrar um risco inexistente faz o time gastar mitigação com fantasma — e o doc perde credibilidade nos riscos que são reais.
- **Incluí "não fazer nada" como alternativa**, ancorada no INC-4412. É o contraponto que justifica o esforço.

## O que preciso de você

1. **Autores e revisores** — ficaram como `_a definir_` no cabeçalho. Quem assina, e quais áreas revisam? Pela superfície do doc eu sugeriria alguém de Plataforma/Gateway, SRE (pelo Redis no caminho crítico) e alguém de Contas/Customer Success, que é quem vai avisar os enterprise quando o 429 aparecer.
2. **Enterprise "negociado"** — o limite sai de onde na prática (campo no plano, config manual no Kong)? Hoje o doc só diz "negociado por contrato".
3. **`Retry-After`** — devolve segundos fixos, ou o tempo restante da janela? Faz diferença para quem implementa o retry do lado do cliente.
4. **Prazos das fases** — o DD-2026-007 põe uma estimativa em cada etapa ("1 semana"). Se você me der os prazos do shadow mode / free / geral, eu completo.

## Diagrama

Coloquei um diagrama de sequência Mermaid dentro da Proposta, mostrando a requisição passando pelo Kong, o incremento do contador no Redis e os dois desfechos (encaminhar ou 429 com `Retry-After`). Renderiza nativamente no GitHub/GitLab.

**Não validei o Mermaid aqui**: o diagrama nomeia sistemas internos (Kong, o Redis de sessão) e os limites por plano, então evitei o validador hospedado, que renderiza remotamente — e o `mermaid-cli` não está instalado nesta máquina. Confira o render abrindo o arquivo no GitHub/GitLab de vocês, que é privado como o resto do repositório. Se você achar que a exposição é aceitável, aí sim colo no validador hospedado e te devolvo o preview — mas essa chamada é sua.

Não desenhei um diagrama de arquitetura C4: a proposta não muda a topologia (é comportamento novo em um gateway que já existe), e o padrão da casa não usa diagrama. Se quiser um container diagram mostrando gateway, Redis e serviços da API pública, eu escrevo em Structurizr DSL e renderizo.

Uma última sugestão: se o doc for circular fora do time da plataforma, vale um glossário logo depois do cabeçalho para *rps*, *janela deslizante*, *shadow mode* e *enforcing* — digo os termos que um revisor de Contas provavelmente trava. Não adicionei porque o DD-2026-007 não tem essa seção; se topar, eu incluo.
