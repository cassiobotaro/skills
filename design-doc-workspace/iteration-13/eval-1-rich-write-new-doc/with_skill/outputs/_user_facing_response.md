Escrevi o design doc em `docs/design/exportacao-de-relatorios-em-background.md`, com o diagrama de arquitetura renderizado em `docs/design/diagrams/arquitetura-containers.svg`.

**Como ficou estruturado**

- **Contexto** — geração síncrona na request, corte de 30s no gateway, 12% de falha acima de 50 mil linhas e o ticket semanal do suporte.
- **Objetivos** — zerar as falhas por timeout tirando a geração do ciclo de request/response e concluir exportações de até 100 mil linhas.
- **O desenho** — visão geral, diagrama de containers C4 (API, fila no RabbitMQ, worker, S3, serviço de e-mail) e o fluxo em diagrama de sequência, cada um seguido do texto que explica as peças.
- **Trade-offs** — com o custo que vocês aceitaram escrito com todas as letras: o usuário perde o download imediato, inclusive nas exportações pequenas, em troca de um caminho único. Somei duas consequências que caem junto: a entrega passa a depender do e-mail chegar, e há mais peças em produção para operar.
- **Alternativas** — síncrono com timeout maior, BI externo e "não fazer nada" (descartada pelos 12% e pelos tickets), em tabela com o motivo de cada descarte.
- **Preocupações transversais** — Plataforma (fila compartilhada) e Segurança (link assinado com dado de cliente), cada um sugerido como revisor no cabeçalho.

O diagrama de sequência foi validado e você pode editá-lo aqui: [abrir no Mermaid](https://l.mermaid.ai/pVyio1). O diagrama C4 está validado e exportado para SVG a partir do DSL, que ficou dobrado no próprio documento — é a fonte da verdade se a arquitetura mudar.

**O que deixei em branco de propósito** (está tudo na seção "Questões em aberto" no fim do doc, mas as quatro primeiras eu preciso de você para fechar):

1. Quem assina como autor, e quem revisa por Plataforma e por Segurança? O cabeçalho está com "a definir".
2. Em que tecnologia a API e o worker vão ser escritos? Deixei as caixas sem tecnologia no diagrama em vez de chutar.
3. Qual serviço faz o envio do e-mail?
4. O que acontece quando um job falha no meio — tem retentativa, e o usuário fica sabendo? O diagrama de sequência mostra só o caminho feliz; não inventei um `alt` de erro.

Também vale decidir a validade do link assinado (o time de segurança vai perguntar) e como o usuário acompanha uma exportação em andamento, já que a resposta da API não traz mais o arquivo. Se você me responder essas, eu já dobro no documento — e, com o número que prova o objetivo (métrica de timeouts) e o plano de entrega, dá para incluir seções de observabilidade e de deploy, que hoje só existem como pergunta.
