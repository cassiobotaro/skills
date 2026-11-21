Corrigi `due_date` em `billing/invoice.py`. Se o vencimento cair num sábado, ele passa para a segunda-feira seguinte (+2 dias). Se cair num domingo, passa para a segunda (+1 dia). Não executei nem testei o código.

O comentário antigo dizia "weekends included", e o código passou a contradizê-lo. Reescrevi o comentário para descrever a regra nova: o banco só compensa boleto em dia útil.

Acrescentei ao comentário que feriados bancários não são tratados. A função só olha sábado e domingo, e um vencimento em feriado continua caindo no feriado. Se quiser tratar feriados, preciso saber de onde virá o calendário.
