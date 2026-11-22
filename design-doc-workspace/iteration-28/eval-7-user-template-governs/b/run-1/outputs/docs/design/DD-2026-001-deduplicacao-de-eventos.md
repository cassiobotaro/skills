# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | Aguardando resposta, ver Perguntas abertas |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Um novo serviço de deduplicação fica entre o ingestor e o Kafka. Cada evento carrega uma chave idempotente. O serviço guarda essa chave no Redis por 24 horas e descarta todo evento cuja chave já esteja guardada. Só os eventos novos seguem para o Kafka.

### Trade-off aceito

O serviço adiciona um salto ao caminho crítico da ingestão. Estimamos +5ms de latência por evento. O time aceita esse custo em troca de eliminar as duplicatas num único ponto, antes de elas chegarem a qualquer consumidor.

### Alternativas consideradas

O template não tem seção para alternativas, então ela entra aqui, logo depois da proposta.

- **Não fazer nada.** Os relatórios de faturamento continuam inflados por cerca de 4% de duplicatas, e o financeiro continua reclamando.
- **Deduplicar no consumidor.** Descartada porque cada consumidor teria que reimplementar a deduplicação.
- **Usar a idempotência nativa do produtor Kafka.** Descartada porque não cobre o reenvio entre reinícios do produtor.

## Riscos

Aguarda resposta do autor: o único custo estabelecido até aqui é o salto extra de +5ms descrito em Proposta. Os demais riscos e suas mitigações estão na primeira pergunta de Perguntas abertas.

## Plano de rollout

Aguarda resposta do autor, na segunda pergunta de Perguntas abertas.

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (hoje 4%, medido no mês passado).

A latência adicional estimada é de +5ms. Como ela é um custo aceito, a forma de acompanhá-la está na terceira pergunta de Perguntas abertas.

## Perguntas abertas

1. **Riscos.** O que o time acha que pode dar errado com o serviço e como pretende mitigar cada ponto?
2. **Plano de rollout.** Como o serviço entra em produção: em quais fases, com qual critério de avanço e qual critério de rollback?
3. **Métricas de sucesso.** Além da taxa de duplicatas, alguma métrica de latência ou disponibilidade deve ser acompanhada, e com qual limite?
4. **Revisores.** Quais pessoas ou áreas (por exemplo arquitetura, financeiro, quem opera o Redis e o Kafka) devem revisar este documento?
5. **Numeração.** Não havia outros documentos em `docs/design/`, então usei DD-2026-001. Esse é o próximo número da sequência?
