Salvei o doc em `docs/design/DD-2026-001-servico-de-deduplicacao-de-eventos.md`. Ele tem as seis seções do template, na mesma ordem e com os mesmos títulos. Não rodei o `unslop` nem uma revisão de texto depois de escrever.

- **Alternativas e trade-off:** o template não tem seção para isso, então coloquei como subseções `###` dentro de **Proposta**, sem criar seção de topo. Os três itens são: deduplicar no consumidor, idempotência nativa do Kafka e "não fazer nada". O +5 ms está em "Trade-off aceito".
- **Número do doc:** assumi `DD-2026-001`, porque `docs/design/` só tinha o template. Se a sequência for outra, é só trocar o título, a tabela e o nome do arquivo.
- **Seções sem conteúdo:** **Riscos** só traz o salto extra no caminho crítico (+5 ms estimados), que foi o único que você citou. **Plano de rollout** diz apenas que ainda não está definido. Não inventei riscos, mitigações nem fases.
- **Métricas:** duplicatas abaixo de 0,1% (linha de base de 4%) e a latência adicional estimada. Não há limite de latência definido.
- **Perguntas abertas (12):** ficaram no final, agrupadas por seção. As principais são:
  - qual é a chave idempotente e quem a gera;
  - o que acontece se o Redis cair;
  - o porquê das 24 horas;
  - como medir os 4% e os 0,1%;
  - o plano de rollout e de rollback;
  - quem são os revisores.

Não pus diagrama C4 porque o fluxo ainda não tem tecnologias e protocolos definidos. Ficou só um esquema em texto.
