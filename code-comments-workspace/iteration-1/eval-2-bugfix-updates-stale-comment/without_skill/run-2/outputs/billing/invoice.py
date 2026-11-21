from datetime import date, timedelta
from decimal import Decimal


def due_date(issued: date, terms_days: int = 30) -> date:
    # Due terms_days calendar days after issue; if that lands on a weekend,
    # move to the following Monday (the bank only clears boletos on business days).
    due = issued + timedelta(days=terms_days)
    weekday = due.weekday()  # Monday=0 ... Saturday=5, Sunday=6
    if weekday >= 5:
        due += timedelta(days=7 - weekday)
    return due


def late_fee(amount: Decimal, days_late: int) -> Decimal:
    # Contract clause 7.2: 2% flat, charged once, whatever the delay.
    if days_late <= 0:
        return Decimal("0")
    return (amount * Decimal("0.02")).quantize(Decimal("0.01"))
