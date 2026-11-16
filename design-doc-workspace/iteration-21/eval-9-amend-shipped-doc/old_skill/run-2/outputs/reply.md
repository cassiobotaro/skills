Atualizei `docs/design/exportacao-de-relatorios.md` com a mudança do disco local para o S3, usando só o que você me contou.

O que mudou no documento:
- **Solução:** o worker grava o CSV no bucket S3 e o download lê de lá, então qualquer worker atende. Mantive uma subseção "Mudança posterior" com o desenho original e o motivo (o segundo worker causava o 404).
- **Trade-offs:** tirei os itens que não valem mais (arquivo só no worker que o gerou, perda do disco). Acrescentei o que a mudança custa e que o documento original já apontava: dependência nova do S3 e a necessidade de credenciais e política de retenção.
- **Alternativas:** o object storage, antes descartado, agora consta como adotado. O disco local entrou como a solução original que deixou de funcionar com dois workers.
- **Cabeçalho:** "Última atualização" passou para 2026-11-16. Deixei o estado como "Implementado".

Não inventei detalhes que você não deu, então registrei duas perguntas em "Questões em aberto". Pode responder para eu fechar essas lacunas?
1. O cron de 7 dias passa a apagar objetos do bucket, ou a retenção virou uma regra de lifecycle do S3?
2. O download ainda passa pela API, ou o usuário recebe um link direto para o bucket?
3. Há outros custos que o time aceitou com essa mudança (custo do S3, latência, permissões), para eu incluir nos trade-offs?
