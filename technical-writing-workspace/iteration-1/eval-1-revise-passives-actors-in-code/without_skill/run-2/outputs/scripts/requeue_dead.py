"""Move messages from exports.dead back to exports.

    uv run python scripts/requeue_dead.py --dry-run    count the messages, move nothing
    uv run python scripts/requeue_dead.py --limit 50   move at most 50 messages
"""
import argparse
import os

import pika


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.URLParameters(os.environ["QUEUE_URL"]))
    channel = connection.channel()
    moved = 0
    while moved < args.limit:
        method, properties, body = channel.basic_get("exports.dead")
        if method is None:
            break
        if args.dry_run:
            channel.basic_nack(method.delivery_tag, requeue=True)
        else:
            channel.basic_publish(exchange="", routing_key="exports", body=body)
            channel.basic_ack(method.delivery_tag)
        moved += 1
    print(f"{'would move' if args.dry_run else 'moved'} {moved} message(s)")


if __name__ == "__main__":
    main()
