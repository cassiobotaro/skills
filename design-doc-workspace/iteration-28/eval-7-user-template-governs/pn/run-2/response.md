Li o template e não há outros docs em `docs/design/`. Então o número será DD-2026-001. Ainda não criei o arquivo. O template exige Riscos, Plano de rollout e Métricas de sucesso, e não quero preencher essas seções com coisas que você não me disse. Preciso de algumas respostas:

1. **Riscos.** Você citou o +5ms de latência no caminho crítico. O que mais pode dar errado, e como mitigamos?
   - O que acontece com a ingestão se o Redis ou o serviço ficar indisponível? Ela falha aberta (deixa passar duplicatas) ou fechada (bloqueia eventos)?
   - Como o serviço trata eventos com a mesma chave que chegam quase ao mesmo tempo?
   - Há outros riscos que vocês já discutiram?
2. **Plano de rollout.** Como entra em produção?
   - Quais são as fases? Por exemplo, modo sombra que só mede, depois um percentual do tráfego, depois todo o tráfego.
   - Qual o critério para avançar de uma fase para a seguinte?
   - Qual o critério de rollback?
3. **Métricas de sucesso.** Além de duplicatas abaixo de 0,1% (hoje 4%), vocês querem medir mais alguma coisa? Por exemplo, um teto para a latência adicionada (os +5ms são só uma estimativa) ou uma disponibilidade mínima. Também preciso saber como e onde vocês medem a taxa de duplicatas.
4. **Cabeçalho.** Quem são os revisores, ou a arquitetura define depois? Posso deixar o campo vazio.
5. **Perguntas abertas.** Há algo que vocês ainda não sabem? Se quiser, registro como pergunta aberta qualquer item acima que ainda não tenha resposta, em vez de afirmá-lo no texto.

Alguns detalhes que o texto vai trazer:
- **Alternativas e metas.** O template não tem seção para elas. Vou incluir as duas alternativas descartadas e a meta dentro de Proposta e Métricas de sucesso, sem criar seções novas. Se você preferir uma seção própria de "Alternativas consideradas", me avise.
- **"Não fazer nada" como alternativa.** Vou citar essa opção, com o custo que você descreveu (4% de duplicatas inflando o faturamento), sem inventar mais nada sobre ela.
