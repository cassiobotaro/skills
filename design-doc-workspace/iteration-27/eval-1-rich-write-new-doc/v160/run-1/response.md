Criei o design doc em `docs/design/exportacao-de-relatorios-em-background.md`, em português, com estado "Rascunho". Passei o unslop na prosa e não rodei nenhum renderizador de diagrama.

O doc tem cabeçalho, glossário, visão geral, contexto, objetivos, o design, trade-offs, alternativas, preocupações transversais e questões em aberto. O design inclui um diagrama de sequência em Mermaid, sem tecnologia nem protocolo que você não tenha citado.

- **Objetivos:** zerar os timeouts, suportar 100 mil linhas e manter um caminho só, com as exportações pequenas também assíncronas.
- **Trade-offs:** o custo que você aceitou, a perda do download imediato, aparece em destaque.
- **Alternativas:** inclui "não fazer nada", com o motivo sendo só a dor que você descreveu (12% de falha e ticket toda semana). Também inclui timeout maior e BI externo, com os motivos que você deu.
- **Preocupações transversais:** Plataforma (fila compartilhada) e Segurança (PII no link assinado) têm uma seção cada. Os dois entram como revisores.

Não inventei nada que você não tenha dito, então ficou uma lista de questões em aberto, que você pode responder ou repassar aos revisores:
- Autores e nomes dos revisores. O campo de autores está como "A preencher".
- O que fica fora de escopo. A seção existe, mas diz que isso ainda não foi definido.
- Validade do link assinado e retenção do arquivo no S3.
- O que acontece quando um job falha (retentativas, aviso ao usuário).
- Volume esperado de exportações e o que a Plataforma precisa para aceitar a carga na fila.
- Como o usuário acompanha uma exportação em andamento.
- Métricas e alertas que mostram que os timeouts zeraram.
- Exigências de Segurança sobre enviar link com PII por e-mail.
- Rollout em etapas e plano de rollback.

Deixei de fora o diagrama C4 de containers. Dá para adicionar quando a tecnologia de cada caixa estiver definida (por exemplo, o provedor de e-mail e como o worker lê os dados).

Não fiz commit.
