import json
import os

import pika
from fastapi import FastAPI, HTTPException

app = FastAPI()
MAX_ROWS = 100_000


def validate_payload(payload: dict) -> None:
    if "account_id" not in payload:
        raise HTTPException(422, "account_id is required")
    if payload.get("rows", 0) > MAX_ROWS:
        raise HTTPException(413, f"exports above {MAX_ROWS} rows are not supported")


@app.post("/exports", status_code=202)
def create_export(payload: dict) -> dict:
    validate_payload(payload)
    connection = pika.BlockingConnection(pika.URLParameters(os.environ["QUEUE_URL"]))
    channel = connection.channel()
    channel.basic_publish(exchange="", routing_key="exports", body=json.dumps(payload))
    connection.close()
    return {"status": "queued"}
