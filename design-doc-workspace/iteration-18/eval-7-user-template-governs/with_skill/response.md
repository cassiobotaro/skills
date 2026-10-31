Doc salvo em `docs/design/deduplicacao-de-eventos.md`, com o diagrama de containers renderizado em `docs/design/diagrams/deduplicacao-de-eventos-containers.svg`.

Segui o `TEMPLATE.md` à risca: cabeçalho com os mesmos campos e as seis seções na mesma ordem (Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso, Perguntas abertas). Um desvio para você decidir: o template não tem lugar para alternativas nem para trade-offs, e esse conteúdo você me deu e é o que dá valor ao doc a longo prazo. Coloquei os dois como subseções da Proposta ("Trade-offs da solução" e "Alternativas consideradas"), então o esqueleto de primeiro nível continua idêntico ao template. Se o time de arquitetura preferir, movo para uma seção própria ou tiro.

O que está preenchido com o que você me passou: a motivação (4% de duplicatas, relatórios de faturamento inflados, duas reclamações do financeiro), a proposta (serviço entre o ingestor e o Kafka, chave idempotente no Redis por 24h, descarte dos repetidos), o custo aceito (+5 ms no caminho crítico), as três alternativas (não fazer nada, deduplicar no consumidor, idempotência nativa do produtor Kafka) e a meta de 0,1%. O diagrama C4 (Structurizr DSL, validado e exportado com a imagem `structurizr/structurizr:playwright`) e o diagrama de sequência (Mermaid, validado com a imagem `minlag/mermaid-cli`) só contêm o que você descreveu: não coloquei tecnologia no ingestor nem no serviço novo, nem protocolo nas setas. Desenhei produtores e consumidores como sistemas externos ao pipeline; se algum deles é do seu time, me avisa que ajusto.

Duas seções do template ficaram marcadas como pendentes, porque não tenho o conteúdo e não quis inventar: **Riscos** e **Plano de rollout**. O cabeçalho também está sem o número do documento e sem revisores. Para fechar o doc, preciso que você responda:

1. **Riscos**: o que o serviço faz quando o Redis não responde? Deixa o evento passar (aceitando duplicatas nesse período) ou segura a ingestão? Esse é o principal risco que a proposta cria, e a mitigação depende dessa escolha.
2. **Chave idempotente**: qual é ela? Todos os produtores já a enviam hoje, ou precisa ser definida ou derivada do evento? E existe reenvio que chegue mais de 24h depois do original (a janela não pega esse caso)?
3. **Plano de rollout**: entra em fases (por produtor, por tipo de evento, modo de observação sem descartar)? Qual o critério de avanço e qual o rollback?
4. **Medição**: como os 4% foram medidos no mês passado? A meta de 0,1% deve usar a mesma medição.
5. **Cabeçalho**: qual é o próximo número da sequência `DD-2026-<seq>`, e quem revisa? Sugiro os times que operam o ingestor, o Kafka e o Redis, e alguém do financeiro como parte interessada nos relatórios.

Com as respostas eu preencho Riscos, Plano de rollout e o cabeçalho e tiro os itens correspondentes de Perguntas abertas. O doc está em estado Rascunho até lá.
