Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`, em português e com estado "Rascunho". Não commitei nada.

Ele cobre o seguinte:
- **Contexto, objetivos e fora de escopo:** os 12% de falha acima de 50 mil linhas e os tickets semanais entram como contexto. Os objetivos são zerar os timeouts e suportar 100 mil linhas. O download imediato para exportações pequenas é o único item fora de escopo.
- **Design:** a descrição da solução (API enfileira, worker gera em streaming e sobe pro S3, link assinado por e-mail), um diagrama de sequência em Mermaid e uma seção sobre os dados com PII.
- **Trade-offs:** o custo central é o usuário perder o download imediato. Também registrei o worker novo para operar, a carga extra na fila compartilhada e a PII em um objeto no S3 e em um link por e-mail.
- **Alternativas:** fazer nada, síncrono com timeout maior e BI externa, cada uma com o motivo do descarte.
- **Preocupações transversais:** Plataforma e Segurança.

Deixei como questões em aberto os pontos que você não definiu, para não inventar:
- Volume de jobs e isolamento na fila compartilhada.
- Validade do link e retenção do arquivo no S3.
- Quem envia o e-mail.
- Comportamento em falha e retry.
- O que a API responde ao enfileirar, e se o usuário tem como acompanhar o pedido.
- Como medir o "zero timeouts".
- Rollout em etapas e plano de rollback.

Preciso que você confirme ou corrija alguns campos do cabeçalho:
- **Autor:** pus `cassiobotaro`, que vem do git config.
- **Revisores:** pus só as áreas (Plataforma e Segurança), sem nomes.
- **Datas:** criação e atualização estão como 2026-11-22.

Não fiz o diagrama C4 de arquitetura, porque exigiria tecnologias e protocolos que você não passou. Se quiser, me diga o que falta e eu o adiciono. Passei as passadas de `technical-writing` e `unslop` no texto.
