Terminei a atualização e passei o `unslop` na prosa nova. Como o serviço já está em produção, não reescrevi o corpo do design doc aprovado. Ele continua sendo o registro de por que o sistema foi construído daquele jeito. Criei uma emenda curta e liguei os dois documentos.

- **Documento novo:** `docs/design/exportacao-de-relatorios-armazenamento-s3.md`. Registra o que você me disse: os arquivos saíram do disco local do worker e foram para um bucket S3, porque o segundo worker fazia o download cair em quem não tinha o arquivo e devolver 404. Segue a mesma estrutura do doc original, com visão geral, contexto, objetivo, solução, trade-offs e alternativas.
- **Documento original:** só dois ajustes no cabeçalho, uma linha `Emendado por` apontando para a emenda e a `Última atualização` em 2026-11-22.

Não afirmei nada que você não tenha dito. Estas perguntas estão no fim da emenda, na ordem do arquivo:

1. Quando a mudança para o S3 entrou em produção, e quando o segundo worker subiu?
2. Quem são os autores e os revisores da emenda? Deixei os dois campos como "A confirmar".
3. O que essa abordagem piorou, e o que o time decidiu aceitar? Hoje o único custo registrado é depender do S3.
4. Como o download funciona agora? O worker lê do bucket e devolve, ou o usuário baixa direto do S3? O endpoint mudou?
5. A retenção de 7 dias continua? Se continua, quem a aplica?
6. Como o worker acessa o bucket, e quem aprovou? O time de Plataforma foi consultado?
7. O que aconteceu com os arquivos que estavam no disco na hora da mudança?
8. Que outras alternativas o time considerou para resolver o 404?
9. Os dois trade-offs do doc original ainda valem com o S3? Eram a premissa de um único worker e a perda dos arquivos se o disco se perde.
10. A meta de entregar o link em até 5 minutos para até 1 milhão de linhas se mantém com o upload para o S3?

Não fiz commit.
