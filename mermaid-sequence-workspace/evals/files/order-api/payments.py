import os
import uuid

import httpx

PAYGATE_BASE_URL = "https://api.paygate.example.com"


async def charge(card_token: str, amount_cents: int) -> dict:
    """Charge the card through PayGate.

    Returns {"payment_id": str, "status": "approved" | "declined"}.
    PayGate 4xx/5xx responses raise and bubble up as a 500 from our API.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{PAYGATE_BASE_URL}/v2/charges",
            json={
                "card_token": card_token,
                "amount": amount_cents,
                "currency": "BRL",
                "capture": True,
            },
            headers={
                "Authorization": f"Bearer {os.environ['PAYGATE_API_KEY']}",
                "Idempotency-Key": str(uuid.uuid4()),
            },
        )
    resp.raise_for_status()
    return resp.json()
