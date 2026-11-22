O design doc já está em produção, então não vou editar o corpo dele. Ele é o registro de por que o serviço foi construído daquele jeito, e o `.claude/skills/design-doc/SKILL.md` manda tratar uma mudança depois do deploy como um documento novo e curto. Esse documento cita o original e diz o que mudou e por quê. No original eu mudo só duas coisas: uma linha `Amended by` no cabeçalho e a data de *Última atualização*.

Antes de escrever, preciso de algumas respostas. Só você sabe, e eu não quero inventar:

1. **Quando a mudança entrou em produção?** Foi quando vocês subiram o segundo worker? Preciso da data, ou pelo menos do mês.
2. **Como o download funciona agora?** O worker ainda serve `GET /exports/<job_id>/download`, lendo do bucket e devolvendo o arquivo? Ou o endpoint responde com uma URL pré-assinada do S3?
3. **E a retenção de 7 dias?** O cron do worker foi trocado por uma lifecycle rule do bucket? Os 7 dias continuam?
4. **O que essa abordagem piora e o que o time decidiu aceitar?** Pense em custo de storage e de transferência, em credenciais novas, em uma dependência a mais ou em latência no download. O design original dizia que o bucket "exigia credenciais e política de retenção novas", então vale registrar como isso foi resolvido.
5. **Quem assina o documento novo?** O original lista "Time de Relatórios" como autor e Marina Prado (Plataforma) como revisora. Ela revisa essa mudança também?

Você pode responder só ao que sabe. Se algum ponto ficar sem resposta, ele entra como questão em aberto no documento novo.

Se preferir, também posso registrar isso como ADR, já que é uma decisão única e já tomada. A skill de ADR não está instalada aqui, então escrevo um mini-doc no formato de `docs/design/`, a não ser que você diga outra coisa.
