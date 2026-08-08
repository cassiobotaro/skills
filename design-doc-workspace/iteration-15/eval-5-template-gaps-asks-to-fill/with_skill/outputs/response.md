Li o `docs/design/dd-2026-007-cache-de-catalogo.md` para pegar o padrão da casa. A estrutura que os nossos design docs seguem é: **tabela de cabeçalho** (Documento, Estado, Autores, Revisores, Criado em, Última atualização, Tags) → **Resumo** → **Contexto** → **Proposta** (com **Compensações** ✓/✗ dentro dela) → **Riscos** (tabela risco/mitigação) → **Plano de entrega** (fases numeradas).

O que você me deu já preenche bem três dessas seções:

- **Resumo / Contexto** — busca por texto exato com `LIKE` no Postgres, ~30% das buscas terminam sem resultado mesmo com o produto no catálogo, porque a consulta casa string e não sentido ("tênis de corrida amortecido" × "tênis running com amortecimento").
- **Proposta** — embeddings de título e descrição gerados por um modelo de similaridade de sentenças, guardados no pgvector (extensão do Postgres que já usamos), busca vetorial com fallback pro `LIKE` atual quando o score vier baixo.

O resto do esqueleto da casa ainda está vazio, e essas seções são justamente as que dão valor ao doc daqui a seis meses. Prefiro perguntar a inventar:

1. **Compensações — o que piora.** A proposta como veio está só com os ganhos, e um doc nosso sem a coluna `✗` não passa em revisão. O que o time aceitou pagar por essa mudança? Coisas que costumam aparecer nesse tipo de troca: custo/latência de gerar o embedding da query a cada busca, o espaço e o tempo de indexação no Postgres, resultados "parecidos mas errados" que a busca exata nunca traria, e a dependência de um modelo novo em produção. Quais desses o time discutiu e decidiu engolir?

2. **Proposta — os pontos que faltam pra alguém conseguir avaliar o desenho.**
   - Qual modelo de similaridade de sentenças, e ele roda onde: dentro da nossa aplicação, num serviço separado, ou numa API de terceiro?
   - Os embeddings dos produtos são gerados em batch (e reprocessados quando o produto muda) ou no fluxo de escrita do catálogo?
   - O "score baixo" que dispara o fallback tem um limiar definido, ou isso ainda é pra descobrir? Como vocês chegaram nele?

3. **Riscos.** A tabela risco/mitigação do padrão. Quais riscos vocês levantaram no refinamento — qualidade dos resultados, carga extra no Postgres, custo, algo com o catálogo desatualizado — e o que já foi pensado como mitigação?

4. **Plano de entrega.** Isso vai de uma vez ou em fases (indexação offline primeiro, shadow mode comparando com o `LIKE`, fatia do tráfego)? E se der ruim, o rollback é só desligar a busca vetorial e voltar pro `LIKE`?

5. **Cabeçalho.** Quem assina como autor, quem revisa (e de que área — plataforma, dados, SRE?), e o doc já nasce como *Rascunho* ou como *Aprovado*, já que a proposta passou pelo refinamento? O próximo ID da sequência seria **DD-2026-008**.

6. **Alternativas.** O padrão da casa não tem seção de alternativas, mas você disse "a proposta que aprovamos no refinamento" — então houve comparação. Se vocês descartaram algo (busca full-text nativa do Postgres com `tsvector`, Elasticsearch/OpenSearch, um serviço de busca gerenciado, sinônimos manuais, ou simplesmente não fazer nada e conviver com os 30%), vale registrar por que perderam. Seria uma seção a mais que o DD-2026-007 não tem — me diz se você quer que eu saia do padrão nesse ponto ou se prefiro dobrar isso dentro da Proposta.

Se você responder ao menos 1, 3 e 4 (as três seções vazias do padrão), eu escrevo o doc em `docs/design/dd-2026-008-busca-por-similaridade-no-catalogo.md`, na mesma estrutura e no mesmo tom do DD-2026-007. Se preferir, me responde só o que já está decidido e eu marco o resto como pendente no lugar certo, em vez de preencher com texto genérico.
