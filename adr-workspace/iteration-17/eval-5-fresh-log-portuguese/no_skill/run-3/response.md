Documentei a decisão em `docs/adr/0001-rabbitmq-em-vez-de-kafka.md`. O repositório estava vazio, então criei a pasta `docs/adr/` e usei a numeração 0001. Não fiz commit.

O ADR tem status "Aceita" e a data de hoje (2026-11-22). Ele cobre:
- **Contexto:** a experiência da equipe com RabbitMQ, o volume abaixo de 100 msg/s e a ausência de necessidade de retenção.
- **Justificativa:** esses mesmos três pontos.
- **Consequências:** a simplicidade operacional, e o trade-off aceito de abrir mão do replay de eventos.
- **Revisão:** se algum dia for preciso replay ou retenção, isso será um novo ADR.

Acrescentei por conta própria um risco: se o volume crescer muito além do previsto, o RabbitMQ pode deixar de ser adequado. Se não quiser essa linha, é só removê-la.
