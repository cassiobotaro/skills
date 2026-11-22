# Runbook: ExportsDeadLetterHigh

> Os trechos marcados com **[PREENCHER]** dependem de informações que só o time dono do serviço tem (nomes de fila, links, comandos, contatos). Complete antes de publicar.

## O que o alerta significa

A dead letter queue (DLQ) de exports passou do limite de mensagens. Cada mensagem na DLQ é um export que falhou todas as tentativas de processamento e **não será reentregue sozinho**. O usuário que pediu o export provavelmente não recebeu o arquivo.

- **Condição de disparo:** [PREENCHER: expressão/limite do alerta, ex.: profundidade da DLQ > N por M minutos]
- **Fila principal:** [PREENCHER]
- **DLQ:** [PREENCHER]
- **Serviço consumidor (worker de exports):** [PREENCHER]
- **Dashboard:** [PREENCHER link]
- **Logs:** [PREENCHER link/query]

## Severidade e urgência

- A DLQ crescendo **não derruba** o sistema, mas indica perda de exports para clientes.
- Trate como urgente se a DLQ cresce rápido (falha sistêmica) ou se há cliente reclamando.
- Se a DLQ está estável e a fila principal normal, é falha pontual: investigue em horário comercial.

## Passo a passo

### 1. Dimensione o problema (2 min)

1. Abra o dashboard e veja a profundidade da DLQ nos últimos 60 min: está **crescendo** ou **estável**?
2. Veja a fila principal: está acumulando (consumidor parado) ou drenando normalmente?
3. Verifique se houve deploy ou mudança de configuração na última hora: [PREENCHER onde ver].

### 2. Olhe as mensagens e os logs (5 min)

1. Leia 3 a 5 mensagens da DLQ sem removê-las: [PREENCHER comando/console].
2. Procure nos logs do worker os erros do mesmo período: [PREENCHER query].
3. Classifique a causa:

| Sintoma | Causa provável | Ação |
|---|---|---|
| Todas as falhas com o mesmo erro, começou após deploy | Bug na versão nova | Passo 3A |
| Timeout, 5xx ou conexão recusada em dependência (banco, storage, API) | Dependência fora ou lenta | Passo 3B |
| Erro de permissão/credencial (401, 403, token expirado) | Credencial ou acesso quebrado | Passo 3C |
| Erro de validação ou dado inesperado em poucas mensagens | Payload inválido (mensagem "venenosa") | Passo 3D |
| Fila principal parada e sem erro nos logs | Worker fora do ar | Passo 3E |

### 3. Corrija a causa

**3A. Bug após deploy.** Faça rollback para a versão anterior: [PREENCHER comando]. Confirme que novas mensagens deixam de ir para a DLQ antes de seguir para o passo 4.

**3B. Dependência com problema.** Confirme o status da dependência: [PREENCHER]. Se o problema é externo, acompanhe a recuperação e avise o canal de incidentes. Não reprocesse a DLQ enquanto a dependência estiver instável: as mensagens falham de novo.

**3C. Credencial ou acesso.** Verifique expiração/rotação de segredo: [PREENCHER]. Renove ou restaure o acesso e reinicie o worker: [PREENCHER comando].

**3D. Payload inválido.** Não reprocesse essas mensagens. Registre o ID do export e do usuário, e abra um ticket para o time dono: [PREENCHER]. Se for um grupo pequeno, siga para o passo 4 com as demais.

**3E. Worker fora do ar.** Veja o estado do serviço (crash loop, falta de recurso): [PREENCHER comando]. Reinicie e acompanhe os logs por 5 min.

### 4. Reprocesse a DLQ (somente após corrigir a causa)

1. Reenvie **um lote pequeno** (5 a 10 mensagens) para a fila principal: [PREENCHER comando/console de redrive].
2. Confirme que foram processadas e que não voltaram para a DLQ.
3. Reenvie o restante.
4. Mensagens que falharem de novo: trate como 3D.

> Não apague mensagens da DLQ sem registrar o conteúdo ou o ID. Depois de apagadas, não há como recuperá-las. [PREENCHER: período de retenção da DLQ]

### 5. Confirme a resolução

- A profundidade da DLQ voltou ao nível normal: [PREENCHER valor esperado].
- O alerta voltou a OK.
- Nenhuma mensagem nova entrou na DLQ por 15 min.

### 6. Registre

Anote no canal do plantão/ticket: causa, ação tomada, quantidade de exports afetados e se algum cliente precisa ser avisado.

## Quando escalar

Escale se:

- Você não identifica a causa em 30 min.
- A DLQ continua crescendo depois da correção.
- O problema está em dependência de outro time.
- Há dados sensíveis de clientes expostos nas mensagens ou nos logs.

**Contato de escalonamento:** [PREENCHER: time/rotação de plantão do dono do serviço de exports, canal e forma de acionar]. Esta informação não foi fornecida e sem ela o runbook fica incompleto para quem está de plantão.

## Manutenção deste documento

Revise após cada incidente com este alerta. Dono do documento: [PREENCHER].
