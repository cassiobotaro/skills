# Serviço de deduplicação de eventos

| | |
|---|---|
| **Documento** | DD-2026-<seq> (sequência a atribuir pelo time de arquitetura) |
| **Estado** | RASCUNHO |
| **Jira relacionado** | |
| **Issues relacionadas** | |
| **Dono do requisito** | |
| **Desenvolvedores** | Rafael Nunes |
| **Engenheiro de qualidade** | |
| **Engenheiro de suporte** | |
| **Revisores técnicos** | |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |

## 1. Contexto

### 1.1 Descrição

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

Hoje nada no pipeline descarta esses eventos, então o problema continua a cada retry dos produtores e volta a aparecer nos relatórios de faturamento. A proposta é um serviço de deduplicação entre o ingestor e o Kafka, descrito na seção 5.1.

**Objetivo**

- Reduzir os eventos duplicados que chegam ao Kafka para menos de 0,1% (hoje 4%).

**Não-objetivos**

- Pendente: o que fica fora desta entrega? (ver 2.2)

### 1.2 Terminologia

| Termo | Definição |
|---|---|
| Evento duplicado | Evento reenviado pelo produtor (por exemplo, em retry) que repete outro já recebido. |
| Chave idempotente | Chave que identifica um evento de forma única; dois eventos com a mesma chave são o mesmo evento. |
| Ingestor | Componente do pipeline que recebe os eventos dos produtores e os entrega ao Kafka. |
| Serviço de deduplicação | Serviço novo, entre o ingestor e o Kafka, que descarta eventos cuja chave idempotente já foi vista. |
| Janela de deduplicação | Período de 24h em que o Redis guarda a chave de cada evento. |

### 1.3 Atores e cenários

- **Produtores**: reenviam eventos em retry, o que gera as duplicatas.
- **Financeiro**: lê os relatórios de faturamento e sofre com os valores inflados.
- **Consumidores do Kafka**: hoje recebem as duplicatas.

Cenário principal: um produtor reenvia um evento em retry; o serviço de deduplicação reconhece a chave idempotente e descarta o reenvio, e só uma cópia chega ao Kafka.

Pendente: outros atores (time de plataforma que opera o Redis e o Kafka, donos dos consumidores) e cenários (por exemplo, o reenvio chegar depois de 24h). Ver 2.2.

## 2. Desenho funcional

### 2.1 Resumo da funcionalidade

O serviço de deduplicação fica entre o ingestor e o Kafka. Para cada evento, ele consulta a chave idempotente no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave por 24h e deixa o evento seguir para o Kafka.

Para quem consome os eventos, o resultado esperado é um fluxo com menos de 0,1% de duplicatas e, com isso, relatórios de faturamento sem a inflação atual.

### 2.2 Notas, dúvidas e pendências

**Desvantagem conhecida e aceita**

- O serviço é mais um salto no caminho crítico da ingestão. A estimativa é de +5ms de latência (estimativa, ainda sem medição).

**Perguntas em aberto para o autor** (sem resposta na conversa; nada abaixo foi presumido neste documento)

1. Quais são os não-objetivos desta entrega?
2. De onde vem a chave idempotente de cada evento: os produtores já a enviam, ou ela precisa ser definida? Quem a define?
3. O que o serviço faz quando o Redis está indisponível ou lento?
4. O que acontece com um reenvio que chega depois da janela de 24h?
5. Quais clientes (produtores, ingestor, consumidores) precisam mudar, se algum?
6. Como o serviço será implantado e como a funcionalidade pode ser desligada?
7. Quais volumes e limites de carga o serviço precisa suportar?
8. Quais dados dos eventos passam pelo serviço e pelo Redis? Há dados sensíveis?
9. Quais métricas, alertas e logs vão mostrar o serviço saudável ou quebrado?
10. Quem são o dono do requisito, o engenheiro de qualidade, o engenheiro de suporte e os revisores técnicos? Qual o Jira relacionado?

### 2.3 Alternativas consideradas e trade-offs

Esta seção não existe no template da casa. O template não tem lugar para as alternativas e os trade-offs que o time discutiu, então ela entra como subseção extra, sem alterar a ordem nem o esqueleto do template. A decisão de mantê-la é do time de arquitetura.

**Trade-off da solução escolhida**

| | |
|---|---|
| ✓ | Um único ponto deduplica para todos os consumidores. Meta: duplicatas abaixo de 0,1%, contra 4% hoje. |
| ✓ | Cobre o reenvio entre reinícios do produtor. |
| ✗ | Mais um salto no caminho crítico da ingestão, estimado em +5ms de latência. |

O time aceitou o custo da latência em troca da deduplicação central.

**Alternativas**

| Alternativa | Por que perdeu |
|---|---|
| Não fazer nada (**descartada**) | As duplicatas continuam em 4%, inflam os relatórios de faturamento e o financeiro já reclamou duas vezes. |
| Deduplicar no consumidor (**descartada**) | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka (**descartada**) | Não cobre o reenvio entre reinícios do produtor. |
| Serviço de deduplicação com Redis, 24h (**escolhida**) | Ver 5.1. |

## 3. Interação com o usuário

### 3.1 API e protótipos

Pendente: a interface do serviço (como o ingestor o chama, qual campo carrega a chave idempotente, o que o serviço devolve quando descarta um evento) não foi descrita. Ver 2.2, perguntas 2 e 5.

## 4. Mudanças nos clientes

Pendente: não foi estabelecido se produtores, ingestor ou consumidores precisam mudar. Ver 2.2, pergunta 5. Se houver mudança em quem chama o sistema, avisar o time de APIs.

## 5. Desenho técnico

### 5.1 Componentes

O serviço de deduplicação é um componente novo, posicionado entre o ingestor e o Kafka. Ele usa o Redis para guardar a chave idempotente de cada evento por 24h.

![Diagrama de containers: serviço de deduplicação de eventos](diagrams/arquitetura.svg)

> Renderizar na passada manual: a imagem acima ainda não foi gerada. A fonte está na seção abaixo.

<details>
<summary>Fonte do diagrama (Structurizr DSL)</summary>

```
workspace {
    model {
        produtor = softwareSystem "Produtores de eventos" "Enviam eventos e reenviam em retry." "External"

        pipeline = softwareSystem "Pipeline de ingestão" {
            ingestor = container "Ingestor" "Recebe os eventos dos produtores."
            dedup = container "Serviço de deduplicação" "Descarta eventos cuja chave idempotente já foi vista."
            redis = container "Redis" "Guarda a chave idempotente de cada evento por 24h."
            kafka = container "Kafka" "Recebe os eventos sem duplicatas."
        }

        produtor -> ingestor "Envia eventos"
        ingestor -> dedup "Encaminha eventos"
        dedup -> redis "Consulta e grava chaves idempotentes"
        dedup -> kafka "Publica eventos novos"
    }

    views {
        container pipeline "containers" {
            include *
            autolayout lr
        }
    }
}
```

</details>

O produtor envia o evento ao ingestor. O ingestor encaminha o evento ao serviço de deduplicação, que consulta a chave idempotente no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço grava a chave no Redis por 24h e publica o evento no Kafka. As tecnologias de transporte entre os componentes e o formato do evento não foram estabelecidos e ficam fora do diagrama.

### 5.2 Compatibilidade e atualização

Pendente: convivência de versões durante o deploy e migração do que já existe não foram descritas. Ver 2.2, perguntas 5 e 6.

### 5.3 Desempenho e escala

- Estimativa de latência: +5ms por evento, por causa do salto extra no caminho crítico.
- Meta de qualidade: duplicatas abaixo de 0,1%.

Pendente: volume suportado, limites conhecidos, comportamento com o Redis indisponível e como desligar a funcionalidade. Ver 2.2, perguntas 3, 4, 6 e 7.

### 5.4 Segurança

Pendente: superfície nova, permissões e dados sensíveis nos eventos e no Redis não foram descritos. Ver 2.2, pergunta 8.

### 5.5 Observabilidade

Pendente: métricas, logs, traces e alertas não foram definidos. A meta de 0,1% de duplicatas implica ao menos uma métrica da taxa de duplicatas que chegam ao Kafka, mas a forma de medi-la cabe ao autor. Ver 2.2, pergunta 9.

## 6. Critérios de teste

Pendente: os testes exigidos antes do lançamento não foram definidos. O único critério estabelecido é a meta de duplicatas abaixo de 0,1%, medida contra a linha de base de 4%. Ver 2.2, pergunta 10.

## 7. Outros artefatos

Nenhum link informado até agora.
