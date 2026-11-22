Como o serviço já está em produção, não reescrevi o corpo do design doc original. A skill manda registrar a mudança num documento novo e ligar os dois.

- **Documento novo:** `docs/design/exportacao-de-relatorios-armazenamento-s3.md`. Ele nomeia o design original e diz o que mudou: os arquivos saíram do disco do worker e foram para um bucket S3. O motivo é o 404 no download depois que o segundo worker subiu.
- **Documento original:** `docs/design/exportacao-de-relatorios.md` recebeu só a linha `Alterado por` no cabeçalho e a data de atualização (2026-11-22). O corpo ficou como estava.

Nos trade-offs, o documento novo usa só o que o original já tinha escrito. O bucket tira a premissa de um único worker. Em troca, o serviço ganha uma dependência nova, com credenciais e retenção a definir. As duas vantagens que o original listava ("nenhuma dependência nova" e "sem custo de transferência") deixam de valer como estavam escritas. A alternativa "não fazer nada" está registrada, porque o 404 já acontecia.

Não afirmei nada que você não tenha dito. Deixei no fim do documento, em "Questões em aberto", as perguntas abaixo, que só você pode responder:

1. Em que data a mudança entrou em produção?
2. Quem serve o download hoje: o worker lendo do S3, a API ou uma URL pré-assinada? Isso também define o custo de transferência.
3. A retenção de 7 dias continua? Quem apaga os arquivos antigos: o cron do worker ou uma regra de ciclo de vida do bucket?
4. O que aconteceu com os arquivos que estavam no disco no momento da mudança?
5. O `/var/exports` e o cron de limpeza foram removidos?
6. O que o time aceitou como custo do S3: custo financeiro, latência, credenciais?
7. O time avaliou outras saídas, como volume compartilhado, roteamento do download para o worker de origem ou um único worker? Por que perderam?
8. Quem revisa o documento? Segurança ou Infraestrutura precisam olhar o acesso ao bucket e as credenciais?
9. Mais alguma parte do design original mudou além do local de armazenamento?
10. O Time de Relatórios é o autor desta mudança? Usei esse nome porque é o do original.

Rodei o unslop no texto novo e corrigi os trechos em que eu tinha deduzido consequências que você não afirmou, como "elimina o 404".

Não commitei nada.
