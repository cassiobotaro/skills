Olhei o `docs/design/` — tem o `dd-2026-007-cache-de-catalogo.md`, e segui o padrão dele: tabela de cabeçalho com os mesmos campos, e as seções **Resumo → Contexto → Proposta (com ### Compensações) → Riscos (tabela risco/mitigação) → Plano de entrega**, continuando a numeração.

Escrevi em `docs/design/dd-2026-008-rate-limiting-api-publica.md`.

**Duas seções fora do padrão da casa.** O DD-2026-007 não tem onde colocar duas coisas que você me deu, e preferi não jogar fora:

- **Objetivos** (entre Contexto e Proposta) — o "nenhum token excede seu limite por mais de 1s" e o "aguentar um cliente abusivo sem degradar os demais" são objetivos verificáveis, ficariam escondidos dentro do Resumo.
- **Alternativas consideradas** (depois da Proposta) — limitar dentro de cada serviço e o módulo pago do gateway gerenciado, cada uma com o motivo do descarte. É o que faz a decisão auditável daqui a um ano. Incluí também o "não fazer nada", ancorado no INC-4412.

O esqueleto e a ordem da casa continuam intactos, mas o desvio é seu para aceitar — se o padrão for fechado, eu dobro as duas dentro de Resumo e Proposta.

**Duas outras decisões que vale você conferir:**

- **Deixei o falso positivo de NAT compartilhado de fora**, como você disse: o limite é por token, não por IP, então esse risco não existe. Se ele aparecer numa revisão, a resposta está na própria Proposta.
- **Coloquei um diagrama de sequência** (Mermaid, renderiza direto no GitHub) na Proposta, mostrando o caminho dentro do limite e o 429 com `Retry-After`. O DD-2026-007 não tem diagrama; se o padrão for texto puro, é só remover. Validado e com preview aqui: <https://l.mermaid.ai/hatHkT>

**Uma coisa que só você pode preencher:** o cabeçalho está com **Autores** e **Revisores** como `_a definir_`. Quem assina o doc, e quais áreas devem revisar? Pelo que o desenho toca, eu sugeriria alguém de **Plataforma/Gateway** (Kong), **SRE** (o Redis de sessão entrando no caminho crítico de toda requisição da API pública) e alguém de **Contas/Customer Success**, já que a mitigação do 429 em pico depende do time de contas avisar os enterprise.

Um ponto que ficou sem número e talvez valha fechar antes da fase 2: o **tamanho da janela deslizante**. "10 rps" pode ser janela de 1s ou média de 60s — muda bastante o que o cliente sente num pico curto. O shadow mode é o lugar de medir isso.
