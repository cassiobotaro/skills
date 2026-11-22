# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

Os produtores reenviam eventos quando fazem retry, e o pipeline de ingestão recebe essas cópias como se fossem eventos novos. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Um novo serviço de deduplicação fica entre o ingestor e o Kafka. Para cada evento recebido do ingestor, o serviço consulta no Redis a chave idempotente do evento. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço grava a chave no Redis com validade de 24 horas e entrega o evento ao Kafka.

Com isso, a deduplicação acontece uma vez, antes do Kafka. A janela de 24 horas significa que o serviço só reconhece como duplicado um reenvio que chegue até 24 horas depois do primeiro envio.

## Alternativas consideradas

Esta seção não existe no template. Ela registra as alternativas discutidas e o motivo de cada descarte, para que o raciocínio não se perca.

- Deduplicar no consumidor. Descartada. Cada consumidor teria que reimplementar a deduplicação.
- Idempotência nativa do produtor Kafka. Descartada. Ela não cobre o reenvio entre reinícios do produtor.
- Não fazer nada. Mantém os 4% de duplicatas e as reclamações do financeiro. A proposta existe porque esse custo não é aceitável.

## Riscos

O serviço adiciona um salto ao caminho crítico da ingestão. Estimamos +5 ms de latência por evento. A equipe aceitou esse custo em troca de eliminar as duplicatas na origem. Não temos medição, apenas a estimativa.

Falta levantar os demais riscos da proposta e a mitigação de cada um. As dúvidas que já existem estão em Perguntas abertas.

## Plano de rollout

Ainda não definido. As fases, os critérios de avanço e de rollback estão em Perguntas abertas.

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (linha de base: 4% no mês passado).
- Latência adicionada na ingestão, medida e comparada com a estimativa de +5 ms. Ainda não há limite definido (ver Perguntas abertas).

## Perguntas abertas

### Rollout
1. Como o serviço entra em produção: em fases, com tráfego parcial ou em modo sombra antes de descartar de verdade? Qual critério libera cada avanço?
2. Qual condição dispara o rollback?

### Riscos
3. O que acontece com a ingestão se o Redis ficar indisponível: o serviço deixa passar os eventos (e as duplicatas voltam), bloqueia a ingestão ou faz outra coisa?
4. O serviço de deduplicação é replicado? O que acontece se ele cair?
5. O que acontece se o Redis perder as chaves (reinício, evicção) antes das 24 horas?
6. Qual a tolerância de latência da ingestão? O limite de +5 ms foi validado com os produtores ou com quem depende do tempo de resposta?
7. Há risco de descartar um evento legítimo (colisão de chave, ou retry de um evento cuja primeira tentativa falhou depois da gravação da chave)? Como tratamos?

### Proposta
8. Quem gera a chave idempotente e onde ela viaja no evento? Todos os produtores já a enviam?
9. Qual o volume de eventos por segundo e o tamanho esperado do conjunto de chaves no Redis em 24 horas?
10. Reenvios que chegam depois de 24 horas ficam de fora. Medimos quanto das duplicatas atuais chega depois dessa janela?
11. Como a meta de 0,1% será medida (qual consulta, em que período, e sobre qual fonte)?

### Contexto e processo
12. Quais equipes fora a nossa são afetadas (infraestrutura do Redis e do Kafka, produtores, financeiro) e quem precisa revisar o documento?
13. Fora de escopo: há algo que o serviço deliberadamente não vai cobrir (por exemplo, duplicatas geradas dentro do próprio pipeline)?
14. O número de sequência DD-2026-001 está correto? Não havia outros documentos em docs/design/ para continuar a numeração.
