Topa! Mas antes de escrever, preciso de você — um design doc vale pelo registro do *porquê* e dos trade-offs da decisão, e isso eu não posso inventar. "Migrar o monólito pra microserviços" é exatamente o tipo de decisão que costuma ser cara e às vezes desnecessária, então quero te ajudar a documentar a reflexão real, não montar um esqueleto com seções vazias.

O repositório está vazio (não tenho como deduzir a arquitetura atual sozinho), então me responda o que conseguir destas perguntas e eu já escrevo o doc:

1. **Qual é a dor hoje?** O que especificamente o monólito está te impedindo de fazer agora — deploys lentos/arriscados, um trecho que não escala, times se atropelando no mesmo código, outra coisa? E por que resolver *agora*? (Isso vira o problema e justifica o doc — sem isso, "não fazer nada" ganha por padrão.)

2. **Como você vai saber que deu certo?** De preferência um número ou mecanismo concreto: "deploy de pagamentos independente do resto", "reduzir o tempo de build de 40min pra <10min", "isolar o pico do checkout". E tem algo que você explicitamente *não* vai resolver nesta migração?

3. **Como é o monólito hoje e o destino que você imagina?** Stack/linguagem, banco(s), e por onde a migração começaria — você já tem candidatos a primeiros serviços a extrair, ou ainda é "tudo virar microserviço"? Qual parte dessa decisão você está *menos* seguro?

4. **O que mais foi considerado?** Modularizar o monólito sem separar em serviços (modular monolith), extrair só o gargalo, reescrever, ou continuar como está — e por que microserviços ganha? (Mesmo que ainda não tenha decidido, me diz as opções na mesa.)

5. **Quem é afetado fora do seu time?** Banco compartilhado, infra/plataforma (vai precisar de service mesh, CI/CD novo, observabilidade distribuída?), segurança, ou outros sistemas que hoje chamam o monólito direto?

Me manda o que tiver — não precisa responder tudo, qualquer resposta já encurta o que eu te pergunto depois. Com isso eu escrevo o doc centrado nos trade-offs (incluindo o custo que vocês estão aceitando) em vez de um manual de implementação. Onde você quer que eu salve? Sugiro `docs/design/`.
