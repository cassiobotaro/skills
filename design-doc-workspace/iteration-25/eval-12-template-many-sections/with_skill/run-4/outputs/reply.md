Criei `docs/design/servico-deduplicacao-eventos.md`, seguindo o `docs/design/TEMPLATE.md` na ordem e nas seções (1 a 7, mais o cabeçalho). O texto está em português.

**O que está preenchido**, só com o que você disse: problema (4% de duplicatas, financeiro reclamou duas vezes), proposta (serviço entre o ingestor e o Kafka, chave idempotente no Redis por 24h), meta (menos de 0,1%), as duas alternativas descartadas e o "não fazer nada", o custo aceito (+5ms, marcado como estimativa), e você como desenvolvedor. As datas são de hoje (2026-11-16). O diagrama de containers tem a fonte em Structurizr DSL, sem tecnologia nas setas. A imagem `diagrams/arquitetura.svg` é um placeholder, porque não renderizei nada. Renderize na passada manual.

**Desvio do template, para você aceitar ou recusar:** o template não tem lugar para alternativas e trade-offs, então acrescentei a subseção `2.3 Alternativas consideradas e trade-offs`. O resto do esqueleto e da ordem ficou intacto. Se o time de arquitetura não aceitar a 2.3, mova o conteúdo para a 2.2.

**Seções com "Pendente"**, porque você não deu a substância e eu não inventei: não-objetivos, outros atores e cenários, API (3.1), mudanças nos clientes (4), compatibilidade (5.2), segurança (5.4), observabilidade (5.5), critérios de teste (6) e parte de desempenho (5.3). Também ficaram em branco no cabeçalho: Jira, issues, dono do requisito, engenheiros de qualidade e de suporte, revisores, e o número sequencial do DD-2026-<seq>.

**Perguntas para fechar o doc** (também listadas na seção 2.2):
1. Quais são os não-objetivos?
2. De onde vem a chave idempotente? Os produtores já a enviam, ou ela precisa ser definida?
3. O que o serviço faz se o Redis cair ou ficar lento (descarta, deixa passar, bloqueia)?
4. O que acontece com um reenvio depois de 24h?
5. Algum produtor, o ingestor ou algum consumidor precisa mudar?
6. Como será o deploy e como desligar a funcionalidade?
7. Qual o volume de eventos que o serviço precisa suportar?
8. Há dados sensíveis nos eventos que passam pelo serviço e pelo Redis?
9. Quais métricas e alertas vão mostrar que o serviço funciona?
10. Quais testes são exigidos antes do lançamento? Quem são o dono do requisito, QA, suporte e revisores, e qual o Jira?

Não validei nada nem rodei Docker.
