# Runbook: ExportsDeadLetterHigh

> **Antes de publicar:** os trechos marcados com `[PREENCHER: ...]` dependem de informações que não tenho (nomes de fila, dashboards, comandos, contatos). Substitua todos antes de entregar o runbook ao plantão.

## Resumo

O alerta dispara quando a dead-letter queue (DLQ) de exportações acumula mais mensagens do que o limite configurado. Cada mensagem na DLQ é uma exportação que falhou depois de esgotar as tentativas e **não será reprocessada sozinha**. Isso significa que há clientes sem receber o arquivo que pediram.

- **Severidade:** `[PREENCHER: ex. P2 / warning]`
- **Limite do alerta:** `[PREENCHER: ex. > 50 mensagens por 10 min]`
- **Fila/DLQ:** `[PREENCHER: nome da DLQ]`
- **Serviço dono:** `[PREENCHER: time/serviço]`
- **Dashboard:** `[PREENCHER: link]`
- **Logs:** `[PREENCHER: link/query]`

## Impacto

- Usuários que pediram exportação não recebem o arquivo.
- Se a DLQ continuar crescendo, a causa provavelmente segue ativa e novas exportações também estão falhando.
- A DLQ tem retenção de `[PREENCHER: ex. 14 dias]`. Depois disso, as mensagens são perdidas.

## 1. Triagem (primeiros 5 minutos)

Objetivo: descobrir se a DLQ **ainda está crescendo** e **por quê**.

1. Abra o dashboard e veja a tendência da DLQ:
   - **Crescendo:** falha ativa. Vá para o passo 2 com prioridade.
   - **Estável ou caindo:** foi um pico passado. Ainda é preciso entender a causa e reprocessar (passo 4), mas sem urgência de incidente.
2. Veja se houve deploy, mudança de configuração ou migração recente no serviço de exportação ou em suas dependências.
3. Verifique se outros alertas estão disparando junto (banco, storage, fila principal, serviços downstream). Se sim, trate a causa raiz primeiro; a DLQ é consequência.

## 2. Diagnóstico: descobrir o motivo da falha

Inspecione uma amostra de mensagens da DLQ **sem removê-las** (peek/visibility, não consumir):

```
[PREENCHER: comando para inspecionar mensagens da DLQ]
```

Procure o erro registrado nas mensagens ou nos logs do consumidor:

```
[PREENCHER: query de logs filtrando erros do worker de exportação]
```

Classifique pelo padrão do erro:

| Sintoma | Causa provável | Ação |
|---|---|---|
| Timeout / connection refused para banco, storage ou API | Dependência fora ou lenta | Confirme o estado da dependência. Quando ela voltar, reprocesse (passo 4). |
| Erros 403 / credencial expirada / permissão negada | Credencial ou permissão alterada | Renove ou corrija a credencial. Reprocesse. |
| Mesmo erro em todas as mensagens, começou após deploy | Regressão no código | Reverta o deploy (`[PREENCHER: como fazer rollback]`). Reprocesse. |
| Erro em poucas mensagens, sempre do mesmo cliente/tipo de dado | Mensagem "venenosa" (payload inválido, volume excessivo) | Isole essas mensagens, abra bug para o time dono e reprocesse o resto. |
| Out of memory / worker reiniciando | Exportação grande demais para o worker | Veja `[PREENCHER: limite de memória/linhas]`, escale o worker ou abra bug. |
| Sem erro claro, consumidores parados | Workers fora do ar ou sem consumir | Verifique pods/instâncias e reinicie se necessário: `[PREENCHER: comando]`. |

Se nenhuma linha se encaixa, vá direto para a seção **Escalonamento**.

## 3. Mitigação

- **Não apague a DLQ nem faça purge** antes de entender a causa. Apagar significa perder as exportações pedidas pelos clientes.
- Corrija a causa (dependência, credencial, rollback) antes de reprocessar. Reprocessar sem corrigir apenas devolve as mensagens à DLQ.
- Se a falha atinge muitos clientes e não há correção rápida, avise o suporte para comunicar os clientes: `[PREENCHER: canal/contato do suporte]`.

## 4. Reprocessamento

Só depois de a causa estar corrigida:

1. Reprocesse **um lote pequeno** (ex.: 5 mensagens) e confirme que as exportações concluem:
   ```
   [PREENCHER: comando/ferramenta de redrive da DLQ]
   ```
2. Se o lote passou, reprocesse o restante em lotes, acompanhando a taxa de erro no dashboard.
3. Mensagens que voltarem à DLQ depois de corrigida a causa geral são casos individuais. Anote os IDs e abra bug.

## 5. Verificação de que acabou

- A DLQ está em `0` (ou abaixo do limite do alerta) e não volta a crescer por pelo menos `[PREENCHER: ex. 30 min]`.
- Exportações novas concluem normalmente (teste ou veja a métrica de sucesso).
- O alerta voltou ao estado normal.

## Escalonamento

Escale se:

- A causa não for identificada em **30 minutos**.
- A DLQ continuar crescendo depois da mitigação.
- A falha afetar muitos clientes ou houver risco de perda de dados (retenção da DLQ perto do fim).

Contatos:

- **Time dono do serviço de exportações:** `[PREENCHER: canal do Slack/e-mail]`
- **Escalonamento de plantão (secundário):** `[PREENCHER: nome/rotação/PagerDuty]`
- **Suporte ao cliente:** `[PREENCHER: canal]`

## Depois do incidente

- Registre a causa, os IDs afetados e quantas mensagens foram reprocessadas em `[PREENCHER: onde registrar]`.
- Se a causa foi nova, atualize a tabela do passo 2 deste runbook.
- Se o plantão precisou de algo que faltava aqui (permissão, comando, dashboard), corrija o runbook.

---
*Última revisão: `[PREENCHER: data]` — Responsável: `[PREENCHER]`*
