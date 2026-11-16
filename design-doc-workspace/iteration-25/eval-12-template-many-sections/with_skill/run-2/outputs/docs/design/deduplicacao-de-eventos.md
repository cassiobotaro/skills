# Serviço de deduplicação de eventos

| | |
|---|---|
| **Documento** | DD-2026-<seq> (sequência a confirmar, ver 2.2) |
| **Estado** | RASCUNHO |
| **Jira relacionado** | A preencher (ver 2.2) |
| **Issues relacionadas** | A preencher (ver 2.2) |
| **Dono do requisito** | A preencher (ver 2.2) |
| **Desenvolvedores** | Rafael Nunes (autor do documento) |
| **Engenheiro de qualidade** | A preencher (ver 2.2) |
| **Engenheiro de suporte** | A preencher (ver 2.2) |
| **Revisores técnicos** | A preencher (ver 2.2) |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |

## 1. Contexto

### 1.1 Descrição

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento em retries. No mês passado medimos 4% de duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

Este documento propõe um serviço de deduplicação entre o ingestor e o Kafka. O serviço guarda a chave idempotente de cada evento no Redis por 24 horas e descarta os eventos repetidos. Sem ele, os relatórios de faturamento continuam com os números inflados e as reclamações do financeiro seguem sem resposta.

**Objetivos**

- Reduzir as duplicatas que chegam ao Kafka de 4% para menos de 0,1%.

**Não-objetivos**

- A definir (ver 2.2).

### 1.2 Terminologia

| Termo | Definição |
|---|---|
| Chave idempotente | Identificador de um evento que se repete quando o produtor reenvia o mesmo evento. O serviço usa essa chave para reconhecer duplicatas. |
| Duplicata | Evento reenviado pelo produtor em um retry, já recebido antes. |
| Ingestor | Componente do pipeline de ingestão que recebe os eventos dos produtores. |
| Idempotência nativa do produtor Kafka | Recurso do cliente produtor do Kafka contra reenvios. Não cobre reenvio entre reinícios do produtor. |

### 1.3 Atores e cenários

- **Produtores de eventos.** Reenviam eventos em retry, a origem das duplicatas.
- **Financeiro.** Usa os relatórios de faturamento e reclamou duas vezes dos números inflados.
- **Consumidores do Kafka.** Recebem os eventos depois do serviço. Quais são e o que mudam para eles está em aberto (ver 2.2).

## 2. Desenho funcional

### 2.1 Resumo da funcionalidade

O serviço de deduplicação fica entre o ingestor e o Kafka. Para cada evento, ele consulta a chave idempotente no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço grava a chave com validade de 24 horas e entrega o evento ao Kafka. Do ponto de vista dos produtores e dos consumidores, o efeito esperado é que cada evento chegue ao Kafka uma vez dentro da janela de 24 horas.

### 2.2 Notas, dúvidas e pendências

**Desvantagens conhecidas**

- O serviço adiciona um salto no caminho crítico da ingestão. A estimativa é de +5 ms de latência (estimativa do time, sem medição registrada neste documento).
- A janela de dedup é de 24 horas. Um reenvio depois desse prazo passa como evento novo.

**Alternativas consideradas**

| Alternativa | Resultado | Motivo |
|---|---|---|
| Não fazer nada | Descartada | 4% de duplicatas inflam o faturamento e o financeiro já reclamou duas vezes. |
| Deduplicar no consumidor | Descartada | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | Descartada | Não cobre reenvio entre reinícios do produtor. |
| **Serviço de dedup com Redis (escolhida)** | Escolhida | Resolve num ponto único, antes do Kafka, ao custo do salto extra descrito acima. |

**Perguntas em aberto para o autor** (o template exige estas seções; elas ficam marcadas até alguém responder)

1. Cabeçalho: qual o número de sequência do documento (DD-2026-?), o Jira e as issues relacionadas, o dono do requisito, o engenheiro de qualidade, o engenheiro de suporte e os revisores técnicos? Quem mais desenvolve além de você?
2. 1.1: o que fica explicitamente fora do escopo? Sobre a meta de 0,1%, onde ela é medida (no Kafka, nos relatórios) e como?
3. 1.3: quais consumidores e relatórios de faturamento dependem dos eventos? Quais produtores reenviam?
4. 3.1: de onde vem a chave idempotente, quem a gera, e o que o produtor ou o ingestor recebe quando o evento é descartado (sucesso, erro, nada)?
5. 4: o ingestor ou os produtores precisam mudar (por exemplo, passar a enviar a chave)? Os times de API precisam ser avisados?
6. 5.1: o serviço é um processo próprio ou parte do ingestor, e como ele fala com o ingestor, o Redis e o Kafka?
7. 5.2: como o serviço entra em produção sem perder ou duplicar eventos, e como volta atrás?
8. 5.3: qual o volume de eventos e o pico esperado? O que acontece se o Redis cair ou ficar lento: o serviço deixa passar os eventos (e as duplicatas voltam) ou os bloqueia? Dá para desligar o serviço?
9. 5.4: a chave ou o evento contém dados sensíveis? Quem pode acessar o Redis?
10. 5.5: quais métricas, logs e alertas mostram que o serviço funciona (por exemplo, taxa de descarte)?
11. 6: quais testes são exigidos antes do lançamento?
12. 7: há protótipos, planilhas ou documentos relacionados para linkar?

## 3. Interação com o usuário

### 3.1 API e protótipos

A preencher (pergunta 4 em 2.2).

## 4. Mudanças nos clientes

A preencher (pergunta 5 em 2.2).

## 5. Desenho técnico

### 5.1 Componentes

O serviço de deduplicação é um componente novo. Ele recebe os eventos do ingestor, consulta e grava as chaves no Redis e entrega os eventos novos ao Kafka. O diagrama mostra esses quatro elementos. As tecnologias de transporte entre eles não foram definidas e ficam fora do diagrama (pergunta 6 em 2.2).

![Diagrama de contêineres: serviço de deduplicação de eventos](diagrams/architecture.svg)

> Renderizar na passada manual: a imagem acima ainda não foi gerada.

<details>
<summary>Código-fonte do diagrama (Structurizr DSL)</summary>

```
workspace {
    model {
        ingestor = softwareSystem "Pipeline de ingestão" "Recebe os eventos dos produtores" {
            ingestorApp = container "Ingestor" "Recebe eventos dos produtores"
            dedup = container "Serviço de deduplicação" "Descarta eventos repetidos pela chave idempotente"
            redis = container "Redis" "Guarda a chave idempotente de cada evento por 24h"
            kafka = container "Kafka" "Recebe os eventos sem duplicatas"
        }
        ingestorApp -> dedup "Envia eventos"
        dedup -> redis "Consulta e grava chaves"
        dedup -> kafka "Entrega eventos novos"
    }
    views {
        container ingestor {
            include *
            autolayout lr
        }
    }
}
```

</details>

O ingestor envia cada evento ao serviço de deduplicação. O serviço consulta a chave no Redis. Se a chave existe, descarta o evento. Se não existe, grava a chave por 24 horas e entrega o evento ao Kafka.

### 5.2 Compatibilidade e atualização

A preencher (pergunta 7 em 2.2).

### 5.3 Desempenho e escala

O serviço entra no caminho crítico da ingestão e a estimativa do time é +5 ms de latência por evento. Volume, limites, comportamento com o Redis indisponível e a forma de desligar o serviço estão pendentes (pergunta 8 em 2.2).

### 5.4 Segurança

A preencher (pergunta 9 em 2.2).

### 5.5 Observabilidade

A preencher (pergunta 10 em 2.2). A meta de duplicatas abaixo de 0,1% indica pelo menos uma métrica a acompanhar: a taxa de duplicatas que chega ao Kafka.

## 6. Critérios de teste

A preencher (pergunta 11 em 2.2).

## 7. Outros artefatos

A preencher (pergunta 12 em 2.2).
