# Design Doc: Serviço de Exportação de Relatórios em Background

| | |
|---|---|
| **Status** | Proposta |
| **Autor(es)** | _(preencher)_ |
| **Revisores** | Time de Plataforma, Time de Segurança |
| **Data** | 2026-06-07 |
| **Times impactados** | Plataforma (fila compartilhada), Segurança (link assinado com PII) |

---

## 1. Resumo

Hoje os relatórios são gerados de forma síncrona, dentro da própria request da API. Relatórios grandes estouram o timeout de 30s do gateway: cerca de **12% das exportações acima de 50 mil linhas falham**, gerando tickets de suporte recorrentes (toda semana).

A proposta é mover a geração de relatórios para um **worker em background**. A API passa a enfileirar um job no RabbitMQ (já existente na infra), um worker gera o arquivo (CSV/XLSX) em streaming, faz upload para o S3 e o usuário recebe por e-mail um **link assinado** para download quando a geração termina.

**Objetivos mensuráveis:**

- Zerar os timeouts de exportação no gateway.
- Suportar exportações de até **100 mil linhas**.

---

## 2. Contexto e problema

### 2.1 Situação atual

```
Cliente → Gateway (timeout 30s) → API (gera relatório síncrono) → resposta com arquivo
```

A geração acontece dentro do ciclo request/response. Conforme o volume de linhas cresce, o tempo de geração ultrapassa o limite de 30s imposto pelo gateway e a request é abortada.

### 2.2 Evidência do problema

- **~12%** das exportações **acima de 50 mil linhas** falham por timeout.
- O suporte abre tickets sobre essas falhas **semanalmente**.
- Não há caminho de recuperação: o usuário simplesmente vê a request falhar e tenta de novo (geralmente falhando de novo).

### 2.3 Por que resolver agora

O problema é recorrente, custa tempo do time de suporte e tende a piorar à medida que os volumes de dados dos clientes crescem. Além disso, há um requisito de negócio de suportar exportações maiores (100 mil linhas) que é inviável no modelo atual.

---

## 3. Objetivos e não-objetivos

### 3.1 Objetivos

1. **Zerar os timeouts de exportação** — nenhuma exportação deve falhar por estourar o timeout do gateway.
2. **Suportar até 100 mil linhas** por exportação sem degradação.
3. **Caminho único** — unificar exportação pequena e grande no mesmo fluxo assíncrono, eliminando a bifurcação de comportamento.

### 3.2 Não-objetivos

- Não estamos construindo uma ferramenta de BI / análise ad-hoc.
- Não estamos mudando o formato dos relatórios (continua CSV/XLSX).
- Não estamos (neste doc) tratando exportações acima de 100 mil linhas — fica como evolução futura (ver §10).
- Não estamos migrando dados nem alterando o esquema das fontes que alimentam os relatórios.

---

## 4. Solução proposta

### 4.1 Visão geral

```
                              (1) POST /exports
  Cliente ───────────────────────────────────────► API
                                                     │ (2) publica job
                                                     ▼
                                              RabbitMQ (fila de exportação)
                                                     │ (3) consome job
                                                     ▼
                                                   Worker
                                                     │ (4) gera CSV/XLSX em streaming
                                                     │ (5) upload S3
                                                     ▼
                                                    S3
                                                     │ (6) gera URL assinada
                                                     ▼
                                              Serviço de e-mail
                                                     │ (7) envia link
                                                     ▼
                                                  Cliente
```

### 4.2 Fluxo detalhado

1. **Cliente solicita exportação.** A API recebe a request (`POST /exports`), valida os parâmetros (filtros, formato, escopo do usuário) e cria um registro de job com status `queued`. Responde **imediatamente** (`202 Accepted`) com o `export_id`.
2. **Enfileiramento.** A API publica uma mensagem na fila do RabbitMQ com o `export_id`, os parâmetros do relatório e o destinatário.
3. **Consumo.** Um worker dedicado consome a mensagem. Marca o job como `processing`.
4. **Geração em streaming.** O worker consulta a fonte de dados de forma paginada/streaming e escreve as linhas no arquivo (CSV ou XLSX) sem carregar todo o conjunto em memória. Isso é o que permite suportar 100 mil linhas com uso de memória controlado.
5. **Upload para S3.** O arquivo é enviado ao S3 num bucket dedicado a exportações, com uma chave que não seja adivinhável (ex.: contém um UUID).
6. **Link assinado.** O worker gera uma **URL pré-assinada** do S3 com expiração curta.
7. **Notificação.** O worker dispara um e-mail ao usuário com o link. Marca o job como `done`.

Em caso de erro em qualquer etapa, o job vai para `failed` e segue a política de retry/DLQ (ver §6).

### 4.3 Mudança de comportamento aceita (trade-off)

Hoje exportações pequenas funcionam na hora (download imediato). Com esta proposta, **toda exportação vira assíncrona**, inclusive as pequenas. O usuário perde o download imediato em troca de um caminho único e confiável.

Decisão consciente: aceitamos esse custo de UX para não manter dois fluxos (síncrono para pequeno, assíncrono para grande), o que dobraria a superfície de manutenção e de bugs. Mitigações de UX em §8.

---

## 5. Alternativas consideradas

### 5.1 Alternativa A — Síncrono com timeout maior _(descartada)_

Aumentar o timeout do gateway e/ou da API para acomodar relatórios grandes.

- **Por que foi descartada:** só empurra o problema. Um timeout maior continua sendo um limite fixo; relatórios ainda maiores voltarão a estourar. Além disso, manter conexões abertas por minutos consome recursos do gateway/API e piora a resiliência (qualquer deploy/restart derruba a geração em andamento).

### 5.2 Alternativa B — Ferramenta de BI externa _(descartada)_

Delegar a geração de relatórios a uma ferramenta de BI de terceiros.

- **Por que foi descartada:**
  - **Custo** — licenciamento/consumo da ferramenta.
  - **Exposição de dados de cliente** — enviar dados (com PII) para uma plataforma externa amplia a superfície de risco e exigências de compliance.

### 5.3 Alternativa escolhida — Worker assíncrono + S3 + link por e-mail

Reaproveita infra existente (RabbitMQ), mantém os dados dentro do nosso perímetro (S3 próprio), escala por número de workers e desacopla a geração do ciclo de request. É a opção que ataca a causa raiz (geração dentro da request) em vez do sintoma (timeout).

---

## 6. Detalhes técnicos

### 6.1 API

- Novo endpoint `POST /exports` → cria o job, publica na fila, retorna `202` com `export_id`.
- Endpoint de consulta `GET /exports/{export_id}` → retorna o status (`queued` | `processing` | `done` | `failed`) e, quando `done`, o link assinado. Útil para a UI poder fazer polling e para reenvio do link sem depender só do e-mail.

### 6.2 Modelo de estado do job

| Status | Significado |
|---|---|
| `queued` | Job criado e publicado na fila |
| `processing` | Worker consumiu e está gerando |
| `done` | Arquivo no S3, link gerado, e-mail enviado |
| `failed` | Falhou após esgotar retries |

Persistir os jobs (ex.: tabela `exports`) com: `export_id`, `user_id`, parâmetros, status, timestamps, `s3_key`, `error` e contagem de tentativas.

### 6.3 Worker

- Processo separado da API, consumindo da fila do RabbitMQ.
- Geração **streaming**: paginar a fonte de dados e escrever incrementalmente no arquivo, evitando carregar 100 mil linhas em memória.
- Upload para S3 (preferir upload multipart/streaming para não materializar o arquivo inteiro em memória/disco quando possível).
- Idempotência: reprocessar o mesmo `export_id` deve sobrescrever/regenerar de forma segura (a chave do S3 deriva do `export_id`).

### 6.4 Fila (RabbitMQ)

- Fila dedicada para exportações.
- **Retry + DLQ:** falhas transitórias (ex.: indisponibilidade momentânea do S3) → retry com backoff; após N tentativas → Dead Letter Queue + status `failed` + alerta.
- A fila é **compartilhada na infra do time de Plataforma** — ponto de coordenação (ver §7).

### 6.5 Armazenamento (S3)

- Bucket dedicado a exportações.
- Chaves não-adivinháveis (UUID no path).
- **Lifecycle policy** para expirar/remover arquivos automaticamente após X dias (dado de cliente não deve persistir indefinidamente).

### 6.6 Link assinado

- URL pré-assinada do S3 com **expiração curta**.
- Como o arquivo pode conter **PII**, o tempo de validade e o controle de acesso precisam ser revisados pelo time de Segurança (ver §7 e §9).

### 6.7 Notificação por e-mail

- E-mail enviado ao usuário ao concluir, contendo o link assinado e a validade.
- Considerar template com aviso de expiração e instrução de como gerar novamente caso expire.

---

## 7. Impacto em outros times

### 7.1 Time de Plataforma — fila compartilhada

A fila de exportação roda na infra de mensageria compartilhada. Pontos a alinhar:

- Capacidade/throughput esperado e isolamento (vhost/fila própria) para que picos de exportação não impactem outros consumidores.
- Política de retry/DLQ e monitoramento.
- Provisionamento e escala dos workers.

### 7.2 Time de Segurança — link assinado com PII

Os arquivos de exportação podem conter PII e o link assinado dá acesso direto ao S3. Pontos a alinhar:

- Tempo de expiração aceitável do link.
- Política de retenção/expurgo dos arquivos no S3.
- Criptografia em repouso (S3) e em trânsito.
- Auditoria de acesso aos arquivos.
- Se a entrega por e-mail (link em texto) é aceitável ou se precisa de uma camada adicional de autenticação no download.

---

## 8. Experiência do usuário (UX)

A principal regressão é a perda do download imediato para exportações pequenas. Mitigações propostas:

- **Feedback claro na UI** ao solicitar: "Sua exportação está sendo gerada e você receberá um link por e-mail."
- **Status consultável** (`GET /exports/{id}`) para a UI mostrar progresso e oferecer o link assim que pronto, sem o usuário precisar sair da tela.
- Para exportações **pequenas e rápidas**, a geração tende a concluir em segundos — a UI pode fazer polling curto e oferecer o download na própria tela quando o job ficar `done`, aproximando-se da experiência atual sem manter um caminho síncrono separado.

> **Pergunta em aberto:** queremos investir nesse polling de UI já na v1, ou v1 entrega só o e-mail e a UX de "quase imediato" fica para depois?

---

## 9. Segurança e privacidade

- Arquivos podem conter **PII** → tratar com cuidado em armazenamento, transporte e acesso.
- Links assinados com expiração curta; chaves não-adivinháveis no S3.
- Criptografia em repouso e em trânsito.
- Lifecycle/expurgo automático no S3.
- Garantir que o job só exporte dados que o **usuário solicitante tem permissão de ver** (a autorização da request original precisa ser preservada/validada na geração).
- Revisão formal do time de Segurança antes do go-live.

---

## 10. Métricas de sucesso e observabilidade

**Métricas de sucesso (objetivos):**

- Taxa de timeout de exportação no gateway = **0**.
- Exportações de **100 mil linhas** concluindo com sucesso de forma consistente.
- Redução/eliminação dos tickets de suporte sobre falha de exportação.

**Observabilidade a instrumentar:**

- Tempo de geração por job (p50/p95/p99) e por faixa de tamanho.
- Profundidade da fila e idade da mensagem mais antiga.
- Taxa de sucesso/falha e volume na DLQ.
- Falhas de upload S3 e de envio de e-mail.
- Alertas para acúmulo na fila e crescimento da DLQ.

---

## 11. Plano de implementação (alto nível)

1. Modelagem e persistência de jobs (`exports`) + endpoints `POST /exports` e `GET /exports/{id}`.
2. Publicação na fila do RabbitMQ a partir da API.
3. Worker: consumo, geração streaming, upload S3, link assinado.
4. Notificação por e-mail.
5. Retry/DLQ, observabilidade e alertas.
6. Revisões com Plataforma (fila) e Segurança (PII/link).
7. Rollout (ver §12) e migração do fluxo atual para o assíncrono.

---

## 12. Riscos e estratégia de rollout

| Risco | Mitigação |
|---|---|
| Fila compartilhada saturando outros consumidores | Isolamento (vhost/fila própria), limites e alertas; alinhamento com Plataforma |
| Vazamento de PII via link assinado | Expiração curta, expurgo, criptografia, revisão de Segurança |
| Regressão de UX (perda do imediato) | Status consultável + polling de UI para concluir rápido |
| Worker como novo ponto de falha | Retry/DLQ, idempotência, escala horizontal, monitoramento |

**Rollout sugerido:** habilitar o fluxo assíncrono atrás de feature flag, começar pelas exportações grandes (onde o ganho é claro e o risco do timeout já existe), validar métricas, e então migrar as pequenas para o caminho único.

---

## 13. Questões em aberto

1. **Polling de UI na v1?** (§8) — entregar só e-mail primeiro, ou já oferecer download na tela para jobs rápidos?
2. **Validade do link assinado** e necessidade de autenticação adicional no download — definição com Segurança.
3. **Retenção dos arquivos no S3** (quantos dias antes do expurgo) — Segurança + produto.
4. **Limite de concorrência / nº de workers** e isolamento da fila — definição com Plataforma.
5. **Comportamento acima de 100 mil linhas** — bloquear, paginar em múltiplos arquivos, ou tratar depois?
