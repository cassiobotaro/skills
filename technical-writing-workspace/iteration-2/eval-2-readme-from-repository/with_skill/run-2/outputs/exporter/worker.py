import json
import os

import boto3
import pika
from cryptography.fernet import Fernet

from exporter.notifier import notify

MAX_ATTEMPTS = 3


def build_csv(job: dict) -> bytes:
    rows = [f"{job['account_id']},{n}" for n in range(job.get("rows", 0))]
    return "\n".join(rows).encode()


def handle(channel, method, properties, body) -> None:
    job = json.loads(body)
    attempts = (properties.headers or {}).get("x-attempts", 0) + 1
    try:
        data = Fernet(os.environ["EXPORT_KEY"]).encrypt(build_csv(job))
        key = f"{job['account_id']}/{method.delivery_tag}.csv.enc"
        boto3.client("s3").put_object(Bucket=os.environ["EXPORT_BUCKET"], Key=key, Body=data)
        notify(job["account_id"], key)
    except Exception:
        target = "exports.dead" if attempts >= MAX_ATTEMPTS else "exports"
        channel.basic_publish(
            exchange="",
            routing_key=target,
            body=body,
            properties=pika.BasicProperties(headers={"x-attempts": attempts}),
        )
    channel.basic_ack(method.delivery_tag)


def main() -> None:
    connection = pika.BlockingConnection(pika.URLParameters(os.environ["QUEUE_URL"]))
    channel = connection.channel()
    channel.basic_consume(queue="exports", on_message_callback=handle)
    channel.start_consuming()


if __name__ == "__main__":
    main()
