# Serviço de deduplicação de eventos

| | |
|---|---|
| **Documento** | DD-2026-001 |
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

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento em retries. No mês passado, 4% dos eventos eram duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

Sem a mudança, as duplicatas continuam entrando no pipeline e os relatórios de faturamento continuam inflados. Cada nova reclamação do financeiro tem a mesma causa.

A proposta é um serviço de deduplicação entre o ingestor e o Kafka. O serviço guarda no Redis a chave idempotente de cada evento por 24 horas e descarta os eventos repetidos.

**Objetivo**

- Reduzir as duplicatas no pipeline de 4% para menos de 0,1%.

**Não-objetivos**

- Nenhum não-objetivo foi informado até aqui. Ver pendência P1 em 2.2.

### 1.2 Terminologia

| Termo | Definição |
|---|---|
| Chave idempotente | Identificador de um evento. Dois eventos com a mesma chave são o mesmo evento. |
| Duplicata | Evento que chega mais de uma vez ao pipeline porque o produtor o reenviou em um retry. |
| Ingestor | Componente do pipeline de ingestão que recebe os eventos dos produtores e os entrega ao Kafka. |
| Produtor | Sistema que envia eventos ao pipeline de ingestão. |
| Redis | Armazenamento onde o serviço guarda as chaves idempotentes já vistas. |
| Kafka | Plataforma de mensagens para a qual o pipeline publica os eventos. |

### 1.3 Atores e cenários

- **Produtores:** reenviam eventos em retry, e esse reenvio gera as duplicatas.
- **Financeiro:** consome os relatórios de faturamento, que hoje saem inflados. Já reclamou duas vezes.
- **Consumidores do Kafka:** hoje recebem as duplicatas e não deduplicam.

Cenário central: um produtor envia um evento, não recebe a confirmação a tempo e o reenvia. O serviço de deduplicação reconhece a chave do segundo envio e o descarta.

Outros cenários (falha do Redis, reenvio depois de 24 horas) não foram descritos. Ver P2 e P3 em 2.2.

## 2. Desenho funcional

### 2.1 Resumo da funcionalidade

Todo evento que o ingestor recebe passa pelo serviço de deduplicação antes de chegar ao Kafka. O serviço consulta a chave idempotente do evento no Redis:

- Se a chave não existe, o serviço a registra com validade de 24 horas e repassa o evento ao Kafka.
- Se a chave existe, o serviço descarta o evento.

Os consumidores passam a receber cada evento uma vez, sem implementar deduplicação por conta própria. Reenvios que chegam depois das 24 horas de validade da chave não são reconhecidos.

### 2.2 Notas, dúvidas e pendências

**Desvantagem conhecida e aceita**

- O serviço é mais um salto no caminho crítico da ingestão. A estimativa do time é de +5 ms de latência por evento. O time aceitou esse custo em troca de eliminar as duplicatas para todos os consumidores num só lugar. A estimativa ainda não foi medida.

**Pendências, a resolver antes de passar o documento para revisão**

- **P1.** O que fica explicitamente fora do escopo deste trabalho?
- **P2.** O que o serviço faz quando o Redis está indisponível: descarta, repassa o evento sem deduplicar ou bloqueia a ingestão?
- **P3.** Como o time trata um reenvio que chega depois da janela de 24 horas?
- **P4.** De onde vem a chave idempotente: o produtor já a envia no evento ou o serviço a calcula? Isso muda a seção 4.
- **P5.** Como o serviço se comunica com o ingestor (biblioteca, chamada de rede, processo separado) e o que o ingestor recebe de volta?
- **P6.** Como o time mede os 4% atuais e vai medir a meta de 0,1%?
- **P7.** Quem são o dono do requisito, o engenheiro de qualidade, o engenheiro de suporte e os revisores técnicos?
- **P8.** Qual é o plano de lançamento (tudo de uma vez ou em etapas) e como desligar o serviço?

## 3. Interação com o usuário

### 3.1 API e protótipos

Sem informação sobre a interface do serviço (P5). Nenhum protótipo existe até aqui.

## 4. Mudanças nos clientes

Sem informação sobre mudanças no código dos produtores e do ingestor (P4, P5). Os consumidores do Kafka não mudam: a motivação de deduplicar fora deles é justamente evitar que cada um reimplemente a lógica.

## 5. Desenho técnico

### 5.1 Componentes

- **Ingestor:** recebe os eventos dos produtores e os envia ao serviço de deduplicação.
- **Serviço de deduplicação (novo):** consulta e grava a chave idempotente no Redis, descarta os repetidos e repassa os demais ao Kafka.
- **Redis:** guarda cada chave idempotente por 24 horas.
- **Kafka:** recebe os eventos já deduplicados.

![Diagrama de contêineres: serviço de deduplicação de eventos](diagrams/arquitetura.svg)

> Renderizar na passada manual: o exportador do Structurizr não foi executado. A imagem acima é um marcador.

<details>
<summary>Código do diagrama (Structurizr DSL)</summary>

```
workspace {
    model {
        produtor = softwareSystem "Produtores" "Enviam eventos e os reenviam em retry."
        pipeline = softwareSystem "Pipeline de ingestão" {
            ingestor = container "Ingestor" "Recebe os eventos dos produtores."
            dedup = container "Serviço de deduplicação" "Descarta eventos com chave idempotente já vista."
            redis = container "Redis" "Guarda as chaves idempotentes por 24h."
            kafka = container "Kafka" "Recebe os eventos deduplicados."
        }
        produtor -> ingestor "Envia eventos"
        ingestor -> dedup "Envia eventos"
        dedup -> redis "Consulta e grava chaves"
        dedup -> kafka "Publica eventos novos"
    }
    views {
        container pipeline "Containers" {
            include *
            autolayout lr
        }
    }
}
```

</details>

O ingestor deixa de publicar direto no Kafka: o serviço de deduplicação ocupa esse lugar no caminho. O serviço é o único componente que lê e escreve no Redis. A tecnologia do serviço e dos protocolos entre os componentes não foi informada e ficou fora do diagrama (P5).

### 5.2 Compatibilidade e atualização

Sem informação sobre convivência de versões durante o deploy, nem sobre a migração do fluxo atual (P8).

### 5.3 Desempenho e escala

- A estimativa de latência adicional é de +5 ms por evento (ver 2.2).
- A janela de deduplicação é de 24 horas.
- Sem informação sobre volume de eventos, tamanho do Redis e limites conhecidos, nem sobre como desligar a funcionalidade (P2, P8).

### 5.4 Segurança

Sem informação sobre superfície nova, permissões ou dados sensíveis. Os eventos alimentam relatórios de faturamento, e o time ainda não disse se a chave idempotente ou o evento contém dados sensíveis (P9 abaixo).

- **P9.** Há dado sensível ou financeiro nos eventos, e o Redis passa a guardá-lo?

### 5.5 Observabilidade

Sem informação sobre métricas, logs e alertas. A meta de duplicatas abaixo de 0,1% só é verificável com uma métrica de duplicatas descartadas e de duplicatas que chegam ao Kafka (P6).

### 5.6 Alternativas consideradas

Esta seção não existe no modelo da casa. Ela foi acrescentada ao fim do desenho técnico para registrar as alternativas que o time discutiu, sem alterar a ordem das demais seções.

**Escolhida: serviço de deduplicação entre o ingestor e o Kafka.**

- ✓ Resolve o problema num só lugar, para todos os consumidores.
- ✗ Adiciona um salto no caminho crítico da ingestão, com +5 ms de latência estimados.

**Não fazer nada.**

- ✗ As duplicatas (4% no mês passado) continuam inflando os relatórios de faturamento, e o financeiro já reclamou duas vezes.

**Deduplicar no consumidor.**

- ✗ Cada consumidor teria que reimplementar a deduplicação. O time descartou a alternativa por isso.

**Usar a idempotência nativa do produtor Kafka.**

- ✗ Não cobre o reenvio entre reinícios do produtor. O time descartou a alternativa por isso.

## 6. Critérios de teste

Critério de aceite derivado da meta: duplicatas abaixo de 0,1%, contra 4% medidos no mês passado. Sem informação sobre testes funcionais, negativos, de carga e de longa duração (P2, P3, P6).

## 7. Outros artefatos

Nenhum artefato relacionado foi informado até aqui.
