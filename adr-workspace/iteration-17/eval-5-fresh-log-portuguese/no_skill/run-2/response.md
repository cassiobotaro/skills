Documentei a decisão em `docs/adr/0001-rabbitmq-em-vez-de-kafka.md`. O repositório estava vazio, então escolhi um formato de ADR simples, com status "Aceita" e a data de hoje.

O documento tem contexto, decisão, justificativa e consequências. Nas consequências, registra que o replay de eventos foi aceito como trade-off. Diz também que, se esse requisito surgir ou o volume crescer bastante, isso será uma nova decisão (um novo ADR). O Kafka aparece como alternativa rejeitada.

O texto usa só o que você me contou. Se vocês avaliaram outras alternativas ou outros critérios, vale acrescentar. Não fiz commit.
