from datetime import date, timedelta
from decimal import Decimal


def due_date(issued: date, terms_days: int = 30) -> date:
    # Due terms_days calendar days after issue. The bank only clears boletos on
    # business days, so a Saturday or Sunday result moves to the following Monday.
    # Bank holidays are not handled.
    due = issued + timedelta(days=terms_days)
    if due.weekday() == 5:  # Saturday
        return due + timedelta(days=2)
    if due.weekday() == 6:  # Sunday
        return due + timedelta(days=1)
    return due


def late_fee(amount: Decimal, days_late: int) -> Decimal:
    # Contract clause 7.2: 2% flat, charged once, whatever the delay.
    if days_late <= 0:
        return Decimal("0")
    return (amount * Decimal("0.02")).quantize(Decimal("0.01"))
