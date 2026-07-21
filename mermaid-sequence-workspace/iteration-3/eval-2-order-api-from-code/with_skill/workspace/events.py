import json
import os

import aio_pika


async def publish_order_created(order_id: int, customer_id: str, total_cents: int) -> None:
    """Publish order.created to the 'orders' topic exchange on RabbitMQ."""
    conn = await aio_pika.connect_robust(os.environ.get("AMQP_URL", "amqp://rabbitmq:5672/"))
    async with conn:
        channel = await conn.channel()
        exchange = await channel.get_exchange("orders")
        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(
                    {
                        "order_id": order_id,
                        "customer_id": customer_id,
                        "total_cents": total_cents,
                    }
                ).encode(),
                content_type="application/json",
            ),
            routing_key="order.created",
        )
