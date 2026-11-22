Escrevi o runbook em português e salvei em `runbook-ExportsDeadLetterHigh.md`. Ele não está pronto para o plantão usar: faltam dados que só vocês têm, e deixei esses pontos como `[PREENCHER: ...]`.

Não conheço o sistema, então não inventei nomes de fila, comandos nem contatos. O que falta preencher:
- o nome da DLQ e o limite do alerta;
- os links do dashboard e dos logs;
- os comandos para inspecionar a DLQ, reprocessar as mensagens (redrive) e fazer rollback;
- **os contatos de escalonamento**: o time dono das exportações, o plantão secundário e o suporte ao cliente;
- o prazo de retenção da DLQ.

Os contatos são o ponto mais importante. Sem eles o plantão fica sem saída quando o diagnóstico não resolve.

A estrutura do runbook:
1. **Resumo e impacto.** Cada mensagem na DLQ é uma exportação que falhou de vez e que algum cliente está esperando.
2. **Triagem em 5 minutos.** Verifica se a DLQ ainda cresce, se houve deploy recente e se há outros alertas disparando junto.
3. **Diagnóstico.** Uma tabela liga o sintoma à causa provável e à ação: dependência fora do ar, credencial expirada, regressão de deploy, mensagem "venenosa", falta de memória ou workers parados.
4. **Mitigação.** Avisa para não fazer purge da DLQ antes de entender a causa e para corrigir a causa antes de reprocessar.
5. **Reprocessamento.** Começa com um lote pequeno e segue em lotes maiores.
6. **Verificação de que acabou.** Lista os sinais de que o problema terminou.
7. **Escalonamento e pós-incidente.** Define quando escalar (por exemplo, causa não identificada em 30 minutos) e o que registrar depois.

Escrevi a tabela de causas a partir de padrões comuns de falha em filas de exportação, não do histórico do seu alerta. Vale ajustá-la com os incidentes reais que vocês já tiveram.
