Corrigi o `due_date` em `billing/invoice.py`. Agora, se o vencimento cair num sábado ou domingo, ele passa para a segunda-feira seguinte. Sábado ganha mais 2 dias e domingo ganha mais 1. Não rodei nem testei o código.

Troquei também o comentário da função, que dizia "weekends included", para descrever a nova regra.

A correção só trata fim de semana. Feriados bancários não entram, então um vencimento em feriado continua caindo no feriado. Se quiser tratar feriados também, preciso de uma lista deles ou de uma biblioteca de calendário.
