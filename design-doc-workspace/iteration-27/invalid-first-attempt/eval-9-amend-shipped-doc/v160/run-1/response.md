Como o serviço está em produção, não vou editar o corpo do `exportacao-de-relatorios.md`. Ele é o registro de por que o sistema foi desenhado assim. A mudança vai num mini-doc novo, com link nos dois sentidos. No original entra só uma linha `Alterado por` no cabeçalho e a *Última atualização*.

Já tenho o motivo (segundo worker, download caindo no worker sem o arquivo e devolvendo 404) e o que mudou (disco local para bucket S3). Faltam alguns fatos que o repositório não traz e que eu não quero inferir:

1. **Quando a mudança entrou em produção?** Preciso da data para o cabeçalho do mini-doc e para a *Última atualização* do original.
2. **Como o download funciona agora?** O `GET /exports/<job_id>/download` continua servido pelo worker, que lê do bucket e devolve o arquivo? Ou devolve uma URL pré-assinada?
3. **Quem grava no bucket e quem apaga?** O worker grava o CSV no bucket? A retenção de 7 dias continua? Se continua, é o cron do worker ou uma lifecycle rule do bucket? Ou a regra mudou?
4. **O que ficou pior e o que o time aceitou?** O original listava como vantagens "nenhuma dependência nova" e "sem custo de transferência". Hoje há credenciais, custo de storage e uma dependência nova. Quais desses custos você quer registrar? Algum outro?
5. **Alguma alternativa foi pesada?** Por exemplo, disco compartilhado, ou roteamento do download para o worker dono do arquivo. Se não, registro só o S3 e o que o original já dizia sobre ele.

Quando você responder, escrevo o mini-doc em `docs/design/`, no mesmo formato do original e em português. Passo o `unslop` no texto e faço o ajuste no cabeçalho do original.
