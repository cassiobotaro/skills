# Lógica de decisão do deploy

Pipeline de deploy: testes → staging → smoke test → canary (5%) → promoção ou rollback.

```mermaid
flowchart TD
    %% Lógica de decisão do deploy, conforme descrita pela equipe.
    start([Deploy iniciado]) --> tests["Executa os testes"]
    tests --> testsOk{"Testes passam?"}
    testsOk -->|Sim| staging["Deploy em staging"]
    testsOk -->|Não| stop([Deploy interrompido])
    staging --> smoke["Smoke test em staging"]
    smoke --> smokeOk{"Smoke test passa?"}
    smokeOk -->|Sim| canary["Sobe canary com 5% do tráfego"]
    smokeOk -->|Não| stop
    canary --> errOk{"Taxa de erro abaixo de 1%<br/>por 10 minutos?"}
    errOk -->|Sim| promote([Promove para 100% do tráfego])
    errOk -->|Não| rollback([Rollback])
```

> Os ramos "Não" de *Testes passam?* e *Smoke test passa?* levam a **Deploy interrompido** por
> interpretação: a descrição original só define o rollback para a etapa do canary. Confirmar se
> uma falha no smoke test também exige rollback do staging.
