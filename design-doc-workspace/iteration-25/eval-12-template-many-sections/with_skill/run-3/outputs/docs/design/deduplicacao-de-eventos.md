# Serviço de deduplicação de eventos

| | |
|---|---|
| **Documento** | DD-2026-<seq> (a definir: ver 2.2) |
| **Estado** | RASCUNHO |
| **Jira relacionado** | |
| **Issues relacionadas** | |
| **Dono do requisito** | |
| **Desenvolvedores** | Rafael Nunes (autor) |
| **Engenheiro de qualidade** | |
| **Engenheiro de suporte** | |
| **Revisores técnicos** | |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |

## 1. Contexto

### 1.1 Descrição

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes. Não fazer nada mantém esse erro nos relatórios de faturamento.

A proposta é um serviço de deduplicação entre o ingestor e o Kafka. Ele guarda a chave idempotente de cada evento no Redis por 24 horas e descarta os eventos repetidos antes que cheguem ao Kafka.

Objetivo:

- Reduzir as duplicatas para menos de 0,1% (hoje: 4%).

Não-objetivos: nenhum foi definido até aqui (ver 2.2).

### 1.2 Terminologia

| Termo | Definição |
|---|---|
| Duplicata | Evento reenviado pelo produtor em um retry, que chega ao pipeline de ingestão mais de uma vez. |
| Chave idempotente | Chave que identifica um evento e permite reconhecer um reenvio dele. |
| Ingestor | Componente do pipeline que recebe os eventos dos produtores e os entrega ao Kafka. |

### 1.3 Atores e cenários

- Produtores: enviam eventos ao ingestor e reenviam o mesmo evento em retry, o que gera as duplicatas.
- Financeiro: usa os relatórios de faturamento, que as duplicatas inflam.
- Consumidores do Kafka: hoje receberiam as duplicatas e teriam que tratá-las cada um por conta própria (ver 5.6).

Os demais atores e cenários estão pendentes (ver 2.2).

## 2. Desenho funcional

### 2.1 Resumo da funcionalidade

O serviço de deduplicação passa a ficar entre o ingestor e o Kafka. Para cada evento recebido, ele consulta a chave idempotente no Redis. Se a chave já foi vista nas últimas 24 horas, o serviço descarta o evento. Caso contrário, registra a chave no Redis por 24 horas e o evento segue para o Kafka.

Quem produz e quem consome eventos não muda de comportamento: os consumidores deixam de ver os repetidos.

### 2.2 Notas, dúvidas e pendências

Desvantagem conhecida: o serviço adiciona mais um salto no caminho crítico da ingestão, com estimativa de +5 ms de latência. O time aceitou esse custo (ver 5.6).

Perguntas em aberto, a responder antes do merge:

1. Qual é o número sequencial deste documento (DD-2026-<seq>)? Só existe o template em `docs/design/`.
2. Quem é o dono do requisito, o engenheiro de qualidade, o engenheiro de suporte e os revisores técnicos? Quais áreas o design toca (por exemplo, segurança e plataforma)?
3. Há Jira ou issues relacionadas?
4. O que fica explicitamente fora do escopo desta entrega?
5. De onde vem a chave idempotente de cada evento: o produtor a envia ou o serviço a calcula? Qual é o formato?
6. O que o serviço faz quando o Redis está indisponível: descarta nada e deixa passar, ou rejeita eventos?
7. Quais são os demais atores e cenários (1.3)?
8. As seções 3.1, 4, 5.2, 5.3 (parte), 5.4, 5.5, 6 e 7 aguardam as respostas descritas em cada uma.

## 3. Interação com o usuário

### 3.1 API e protótipos

Pendente. Perguntas: o serviço expõe uma API nova ou fica transparente entre o ingestor e o Kafka? Ele devolve algum erro ou resposta nova ao produtor quando descarta uma duplicata? Há aviso de depreciação?

## 4. Mudanças nos clientes

Pendente. Perguntas: os produtores, o ingestor ou os consumidores precisam mudar algo (por exemplo, enviar a chave idempotente)? O time de APIs foi avisado?

## 5. Desenho técnico

### 5.1 Componentes

- Serviço de deduplicação (novo): recebe os eventos do ingestor, consulta e grava a chave idempotente no Redis e encaminha ao Kafka só os eventos que ainda não viu.
- Redis: guarda a chave idempotente de cada evento por 24 horas.
- Ingestor: passa a entregar os eventos ao serviço de deduplicação em vez de enviá-los direto ao Kafka.
- Kafka: recebe os eventos que o serviço encaminha.

Pendentes: o protocolo entre o ingestor e o serviço, a tecnologia do serviço e como ele roda (ver 2.2).

### 5.2 Compatibilidade e atualização

Pendente. Perguntas: como o ingestor e o serviço convivem durante o deploy? Como migrar o que existe, e como voltar ao fluxo atual (ingestor direto ao Kafka) se algo falhar?

### 5.3 Desempenho e escala

O serviço adiciona cerca de 5 ms de latência ao caminho crítico da ingestão (estimativa do time, ainda sem medição).

Pendente. Perguntas: qual é o volume de eventos por segundo e o tamanho esperado do Redis com 24 horas de chaves? Como desligar a funcionalidade?

### 5.4 Segurança

Pendente. Perguntas: o serviço traz superfície nova ou permissões novas? A chave idempotente ou o evento carregam dados sensíveis que o Redis passaria a guardar? Há eventos de auditoria?

### 5.5 Observabilidade

Pendente. Perguntas: quais métricas, logs e alertas mostram que o serviço funciona (por exemplo, a taxa de duplicatas descartadas, a taxa que chega ao Kafka e a latência adicionada)?

### 5.6 Alternativas consideradas e trade-offs

Esta seção não existe no template. Foi acrescentada ao fim do desenho técnico porque o template não tem lugar para alternativas e trade-offs. O restante do template segue sem alteração.

Trade-off aceito: o serviço adiciona mais um salto no caminho crítico da ingestão, estimado em +5 ms de latência. Em troca, o time busca levar as duplicatas de 4% para menos de 0,1%.

| Alternativa | Resultado | Motivo |
|---|---|---|
| Serviço de deduplicação entre o ingestor e o Kafka (proposta) | Escolhida | Atende a meta e trata a duplicata uma vez, num lugar só, ao custo de +5 ms de latência. |
| Deduplicar no consumidor | Descartada | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | Descartada | Não cobre o reenvio entre reinícios do produtor. |
| Não fazer nada | Descartada | As duplicatas (4% no mês passado) continuam inflando os relatórios de faturamento, e o financeiro já reclamou duas vezes. |

## 6. Critérios de teste

Pendente. Perguntas: quais testes funcionais, negativos, de carga e de longa duração o time exige antes do lançamento? Como o time vai verificar a meta de menos de 0,1% de duplicatas?

## 7. Outros artefatos

Pendente. Não há links, protótipos ou documentos relacionados até aqui.
