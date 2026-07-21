from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from db import save_order
from events import publish_order_created
from payments import charge

app = FastAPI(title="Order API")


class OrderItem(BaseModel):
    sku: str
    quantity: int = Field(gt=0)
    unit_price_cents: int = Field(gt=0)


class OrderIn(BaseModel):
    customer_id: str
    card_token: str
    items: list[OrderItem] = Field(min_length=1)


@app.post("/orders", status_code=201)
async def create_order(order: OrderIn):
    total_cents = sum(i.unit_price_cents * i.quantity for i in order.items)

    payment = await charge(order.card_token, total_cents)
    if payment["status"] == "declined":
        raise HTTPException(status_code=402, detail="payment declined")

    order_id = await save_order(order, payment["payment_id"], total_cents)

    # fire-and-forget: the API response does not wait for consumers
    await publish_order_created(order_id, order.customer_id, total_cents)

    return {"order_id": order_id, "status": "confirmed", "total_cents": total_cents}
