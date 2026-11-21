from datetime import date, timedelta
from decimal import Decimal


def due_date(issued: date, terms_days: int = 30) -> date:
    # Due terms_days calendar days after issue, weekends included.
    return issued + timedelta(days=terms_days)


def late_fee(amount: Decimal, days_late: int) -> Decimal:
    # Contract clause 7.2: 2% flat, charged once, whatever the delay.
    if days_late <= 0:
        return Decimal("0")
    return (amount * Decimal("0.02")).quantize(Decimal("0.01"))
