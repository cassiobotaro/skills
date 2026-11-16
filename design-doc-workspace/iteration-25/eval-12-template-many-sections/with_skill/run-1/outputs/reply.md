Criei `docs/design/deduplicacao-de-eventos.md` seguindo o `docs/design/TEMPLATE.md` na ordem e com todas as seções.

Não consegui te fazer perguntas neste turno. Onde você não deu informação, a seção diz que não há informação e aponta para uma pendência numerada (P1 a P9) em 2.2. Não preenchi nada com texto de enchimento nem com suposição.

**O que ficou preenchido com o que você disse:** contexto e objetivo (4% de duplicatas, financeiro, meta abaixo de 0,1%), funcionalidade, componentes, o custo aceito (+5 ms), as duas alternativas descartadas e "não fazer nada".

**Desvio do modelo, para você aceitar ou não:** o modelo não tem lugar para alternativas. Acrescentei a seção 5.6 "Alternativas consideradas", dentro do Desenho técnico, sem mexer na ordem das demais.

**Perguntas que preciso que você responda (resumo das pendências):**
1. O que está fora do escopo?
2. O que o serviço faz se o Redis cair?
3. Como tratar um reenvio depois das 24h?
4. A chave idempotente já vem do produtor ou o serviço a calcula? Há mudança nos clientes?
5. Como o serviço se integra ao ingestor (biblioteca, chamada de rede, processo) e qual a tecnologia?
6. Como vocês medem os 4% e vão medir os 0,1%? Há métricas e alertas?
7. Quem são o dono do requisito, o engenheiro de qualidade, o de suporte e os revisores? Há Jira ou issues?
8. Como será o lançamento e como desligar o serviço?
9. Há dado sensível ou financeiro nos eventos que o Redis passaria a guardar?

**Outras observações:**
- O número do documento `DD-2026-001` é um palpite, porque a pasta só tinha o modelo. Ajuste se houver outra numeração.
- Pus você em "Desenvolvedores", já que disse ser o autor. Os demais campos do cabeçalho ficaram em branco.
- O diagrama (Structurizr DSL, dobrado em `<details>`) não foi renderizado. A imagem `diagrams/arquitetura.svg` é um marcador para a passada manual. Deixei a tecnologia de serviço e protocolos fora do diagrama porque você não as informou.
