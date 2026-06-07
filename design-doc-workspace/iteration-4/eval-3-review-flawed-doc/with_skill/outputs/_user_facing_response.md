Revisei o `docs/design/fanout-de-notificacoes.md`. O design em si está bom — a estrutura do fanout é clara. O que falta no documento são as coisas que dão valor de longo prazo a um design doc: os **custos aceitos** (trade-offs), as **alternativas** descartadas e **objetivos mensuráveis**. Apliquei direto tudo o que era estrutura/clareza e deixei marcado com `<!-- TODO -->` o que depende de você.

## Melhorias aplicadas (já no arquivo)

- **Adicionei um glossário** logo após o cabeçalho. O doc usa fanout, CDC, exchange, DLQ, TPS, SLA, provider, canal — termos em que um revisor de outro time tropeça. Definidos antes do primeiro uso.
- **Enxuguei a visão geral.** Estava num parágrafo só misturando contexto + solução + objetivos. Agora a visão geral é alto nível e sem detalhes.
- **Criei a seção "Escopo e contexto"** com o cenário atual (cron sequencial, leitura da tabela `notifications`, providers chamados um a um) que estava espremido dentro da visão geral — é aí que ele situa o leitor.
- **Corrigi o diagrama:** o texto diz "DLQ por canal", mas o fluxo só mostrava DLQ de push e e-mail. Adicionei a DLQ do in-app.
- **Escrevi a prosa que explica o diagrama** (todo diagrama precisa de texto: o que cada componente faz e como interagem). Marquei que ele não foi validado por ferramenta de renderização.
- **Reescrevi "Fora de escopo".** Os itens ("o sistema não deve ser lento / não deve perder notificações") eram objetivos negados, não exclusões — não excluem nada. Substituí por candidatos a exclusões reais (modelo de dados, novos canais, UI de preferências) para você confirmar.
- **Reformulei "Objetivos"** no formato mensurável + mecanismo (ex.: "reduzir atraso processando canais em paralelo por fila — alvo: P99 < N s"), com os números em TODO.
- **Cabeçalho:** adicionei linhas de Revisores e Tags, atualizei "Última atualização" para 2026-06-07, e marquei que "Autor: Time de Mensageria" deveria nomear pessoas.
- **Adicionei as seções que faltavam** (Trade-offs, Alternativas, Preocupações transversais, Testabilidade e observabilidade, Questões em aberto) com esqueleto e o que se infere do desenho — para você preencher, não inventei fatos.

## Perguntas para o autor (preciso da sua resposta)

1. **Trade-offs — qual o custo aceito?** A seção "Solução" abria com "mais escalável, robusta e fácil de manter", sem nenhuma contrapartida — isso é argumento de venda. O que piorou em troca? Confirme/ajuste os custos que listei: nova dependência de broker + CDC para operar, entrega assíncrona/sem ordem garantida entre canais, e risco de duplicidade (at-least-once) exigindo idempotência. Como vocês garantem idempotência nos workers?
2. **Números do problema e dos objetivos.** Quanto a lentidão dói hoje (fila acumulada, atraso médio/P99, algum incidente)? Qual é o SLA de entrega em números? Qual volume no pico o sistema precisa sustentar?
3. **Alternativas consideradas.** O que mais foi avaliado além do fanout com filas? Em especial: por que "não fazer nada" (manter o cron) não serve, e foi cogitado paralelizar dentro do próprio serviço (pool de threads) sem filas? Qual broker foi escolhido e por que venceu os comparados?
4. **Times impactados (preocupações transversais).** Quem opera o broker/infra e há capacidade? Quem é dono do banco que o CDC vai ler (e essa carga extra foi alinhada)? Quais são os limites de TPS contratados por provider?
5. **Plano de implantação / rollback.** Durante a migração, os dois modelos (cron e filas) convivem ou há corte? Há rollback se uma etapa falhar?
6. **Cabeçalho.** Quem são as pessoas autoras (não só o time) e quais revisores por área (Plataforma/Infra, Dados/CDC) devem revisar?

É só responder o que quiser destas e eu incorporo no documento, removendo os TODOs correspondentes.
