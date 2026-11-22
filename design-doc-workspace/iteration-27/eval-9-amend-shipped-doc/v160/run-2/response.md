Atualizei `docs/design/exportacao-de-relatorios.md`, o único documento do repositório sobre o serviço. Mantive a estrutura e a voz do autor e não rodei nenhum comando.

- **Solução:** o worker grava o CSV no bucket S3 e qualquer worker atende o download. Acrescentei a subseção "Mudança do disco local para o S3", com o motivo: o segundo worker e o 404 no download.
- **Trade-offs:** tirei os itens que valiam só para o disco local, como "nenhuma dependência nova", "um único worker" e "perde o disco, perde os arquivos". Entrou a dependência nova do bucket.
- **Alternativas:** o disco local virou "solução original, substituída". A alternativa do bucket agora diz que foi descartada na primeira versão e adotada depois.
- **Cabeçalho:** "Última atualização" passou para 2026-11-22.

**Pontos em aberto, marcados como `TODO` no texto e listados em "Questões em aberto":**
1. Nome do bucket e chave do objeto.
2. Quem entrega o arquivo no download: o worker lê do S3 e devolve, ou devolve uma URL pré-assinada. Também falta saber como o serviço obtém as credenciais.
3. Retenção atual. O texto original dizia 7 dias, com um cron do worker apagando os arquivos, e não sei se isso continua valendo no bucket.
4. Data da mudança e link do PR ou do ticket.

Removi o item "download sem custo de transferência de storage externo", que só valia para o disco. Não sei se o novo download tem esse custo, então não escrevi nada no lugar.

Assumi que o leitor é quem opera ou mantém o serviço, e escrevi em português, como o resto do documento. Me passe os quatro pontos acima que eu preencho os `TODO`.
