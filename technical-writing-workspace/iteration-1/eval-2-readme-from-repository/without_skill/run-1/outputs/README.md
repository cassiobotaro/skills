# exporter

A service that builds CSV exports in the background. The gateway accepts an export request and queues it. The worker generates the CSV, encrypts it, uploads it to S3, and emails the requester a download link.

For the request lifecycle in prose, see [docs/pipeline.md](docs/pipeline.md).

## How it works

1. `POST /exports` (the gateway, `exporter/gateway.py`) validates the payload and publishes it to the `exports` RabbitMQ queue. It returns `202 {"status": "queued"}`.
2. The worker (`exporter/worker.py`) consumes `exports`, builds the CSV, encrypts it with Fernet, and uploads it to the S3 bucket as `<account_id>/<delivery_tag>.csv.enc`.
3. The notifier (`exporter/notifier.py`) creates a presigned S3 URL valid for 24 hours. It emails the URL through SES to `<account_id>@accounts.example.com`.
4. If processing fails, the worker republishes the job with an incremented `x-attempts` header. On the third failed attempt the job goes to `exports.dead`.

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- A RabbitMQ broker with the `exports` and `exports.dead` queues. The code does not declare them, so create them beforehand.
- An S3 bucket and AWS credentials that can write to it, sign `get_object` URLs, and send mail through SES.

## Setup

```bash
make setup
```

## Configuration

Both processes read their configuration from environment variables.

| Variable | Used by | Purpose |
|---|---|---|
| `QUEUE_URL` | gateway, worker, `scripts/requeue_dead.py` | AMQP URL of the RabbitMQ broker |
| `EXPORT_BUCKET` | worker, notifier | S3 bucket for the encrypted files |
| `EXPORT_KEY` | worker | Fernet key used to encrypt each file |
| `MAIL_FROM` | notifier | Sender address for the SES email |

boto3 reads AWS credentials and region from its usual sources.

## Running

Start the gateway and the worker in separate terminals:

```bash
make run-gateway   # HTTP API on port 8080
make run-worker    # queue consumer
```

Request an export:

```bash
curl -X POST localhost:8080/exports \
  -H 'content-type: application/json' \
  -d '{"account_id": "acme", "rows": 500}'
```

| Status | Meaning |
|---|---|
| `202` | The job was queued |
| `422` | `account_id` is missing |
| `413` | `rows` is above 100,000 |

## Tests

```bash
make test
```

## Operations

**Failed exports.** A job that fails three times lands in `exports.dead`. The Prometheus alert `ExportsDeadLetterHigh` (`deploy/alerts.yaml`) pages when the queue holds more than 10 messages for 5 minutes.

**Requeueing.** After you fix the cause, move messages back to `exports`:

```bash
uv run python scripts/requeue_dead.py --dry-run    # count the messages, move nothing
uv run python scripts/requeue_dead.py --limit 50   # move at most 50 (default 100)
```

The script needs `QUEUE_URL`. Requeued messages are published without the `x-attempts` header, so they get three new attempts.

## Layout

```
exporter/   gateway.py (API), worker.py (consumer), notifier.py (email)
scripts/    requeue_dead.py
deploy/     alerts.yaml (Prometheus alert rules)
docs/       pipeline.md
```
