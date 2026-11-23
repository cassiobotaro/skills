# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-23 |
| **Última atualização** | 2026-11-23 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas.

As duplicatas inflam os relatórios de faturamento. O financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação entre o ingestor e o Kafka. O ingestor entrega cada evento ao serviço, e o serviço decide se o evento segue para o Kafka ou se é descartado.

Para decidir, o serviço guarda no Redis a chave idempotente de cada evento por 24 horas. Se a chave já existe, o evento é um repetido e o serviço o descarta. Se não existe, o serviço registra a chave e o evento segue para o Kafka.

Como a deduplicação acontece antes do Kafka, os consumidores recebem o fluxo já sem repetidos e não precisam tratar duplicatas.

### Alternativas consideradas

Esta seção não existe no template. Ela registra as alternativas discutidas, para que o motivo do descarte fique com o documento.

- **Deduplicar no consumidor.** Cada consumidor teria que reimplementar a deduplicação. Descartada.
- **Idempotência nativa do produtor Kafka.** Não cobre o reenvio entre reinícios do produtor, que é um dos casos que queremos resolver. Descartada.

### Trade-off aceito

O serviço é mais um salto no caminho crítico da ingestão. Estimamos +5 ms de latência por evento. O time aceita esse custo em troca de eliminar as duplicatas num ponto central.

## Riscos

- **Latência no caminho crítico.** O novo salto adiciona cerca de 5 ms (estimativa, ainda não medida). Mitigação: medir a latência real no rollout e comparar com a estimativa.
- **Demais riscos.** Ainda não foram levantados. Ver Perguntas abertas.

## Plano de rollout

Ainda não definido. Ver Perguntas abertas.

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (hoje, 4%).
- Latência adicionada à ingestão medida e comparada com a estimativa de +5 ms.

## Perguntas abertas

Riscos
1. O que acontece com a ingestão se o Redis ficar indisponível: o serviço deixa passar os eventos sem deduplicar (fail-open) ou bloqueia a ingestão (fail-closed)?
2. Qual é o efeito de perder as chaves do Redis (reinício, eviction, falha)? Quais riscos de corrupção ou perda de eventos o time considera?
3. O serviço passa a ser ponto único de falha da ingestão? Como ele escala e quantas instâncias rodam?

Proposta
4. Como se define a chave idempotente: quem a gera (o produtor ou o serviço) e de quais campos ela é composta?
5. O registro da chave acontece antes ou depois da publicação no Kafka? Isso define o que ocorre se a publicação falhar depois de a chave ser gravada.
6. Duplicatas que chegam depois de 24 horas passam. O time aceita essa janela?
7. Falta um diagrama dos componentes e do fluxo (ingestor, serviço, Redis, Kafka). Ele precisa de detalhes de tecnologia e protocolo que não foram informados.

Plano de rollout
8. Quais são as fases de entrada em produção (por exemplo, modo sombra, depois porcentagem do tráfego), o critério para avançar entre fases e o critério de rollback?

Métricas e documento
9. Como a taxa de duplicatas é medida hoje (os 4%), e onde vamos medir a meta de 0,1%? Existe um limite de latência além dos +5 ms estimados?
10. Quem são os revisores deste documento (arquitetura, financeiro, donos dos produtores)? Há outros times impactados?
