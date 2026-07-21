import os

import asyncpg

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(os.environ["DATABASE_URL"])
    return _pool


async def save_order(order, payment_id: str, total_cents: int) -> int:
    pool = await get_pool()
    row = await pool.fetchrow(
        """
        INSERT INTO orders (customer_id, payment_id, total_cents, status)
        VALUES ($1, $2, $3, 'confirmed')
        RETURNING id
        """,
        order.customer_id,
        payment_id,
        total_cents,
    )
    return row["id"]
