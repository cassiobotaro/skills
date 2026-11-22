Rafael, o doc está salvo em `docs/design/deduplicacao-de-eventos.md`. Ele segue o `TEMPLATE.md` na ordem original: cabeçalho, Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.

- **Motivação e Proposta:** escrevi só o que você contou. Isso inclui os 4% de duplicatas, as duas reclamações do financeiro, o serviço entre o ingestor e o Kafka, a chave no Redis por 24h e o descarte de repetidos.
- **Seção extra:** o template não tem lugar para os trade-offs nem para as alternativas que você discutiu. Coloquei os dois como subseções dentro de Proposta, com "não fazer nada" incluído. O esqueleto e a ordem do template ficaram intactos. Se a arquitetura não aceitar subseções extras, mova ou remova.
- **Riscos:** só consta a latência de +5ms no caminho crítico, que você aceitou.
- **Métricas de sucesso:** a meta de duplicatas abaixo de 0,1% (hoje 4%) e a latência adicional.
- **Plano de rollout:** só diz que ainda não foi definido e remete às perguntas, porque você não passou nada sobre ele. Não inventei fases nem critérios.
- **Revisores:** o campo está vazio.
- **Cabeçalho:** o número DD-2026-001 é um palpite meu, porque a pasta só tem o template. Criado em e Última atualização: 2026-11-22.

As 9 perguntas estão no fim do doc, na seção Perguntas abertas. As principais:
- O que acontece se o Redis cair ou ficar lento.
- Como mitigar os +5ms e qual é o teto aceitável.
- Como será o rollout e o rollback.
- Quem define a chave idempotente.
- Quem deve revisar o doc.

Não rodei o `unslop` porque ele não está disponível aqui. Revisei o texto à mão, sem travessões e sem ênfases desnecessárias.
