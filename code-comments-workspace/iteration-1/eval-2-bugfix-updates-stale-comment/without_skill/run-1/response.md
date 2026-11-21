Corrigi o `due_date` em `billing/invoice.py`. Agora, se o vencimento calculado cair no sábado ou no domingo, ele passa para a segunda-feira seguinte. Em outros dias da semana nada muda. Atualizei também o comentário da função, que dizia "weekends included".

Não rodei nenhum teste nem executei o código. A conta é simples: `weekday()` retorna 5 para sábado e 6 para domingo, e somar `7 - weekday` dias leva os dois à segunda.

A correção só trata fim de semana. Feriados bancários continuam de fora. Se o banco também não compensa nesses dias, é preciso uma lista de feriados.
