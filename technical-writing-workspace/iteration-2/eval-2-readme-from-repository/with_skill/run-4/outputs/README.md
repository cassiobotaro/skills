# exporter

`exporter` builds CSV exports of account data in the background. A client posts an export
request to an HTTP gateway, a worker generates and encrypts the CSV, uploads it to an S3
bucket, and emails the account a download link that works for 24 hours.

It has two processes: the gateway (FastAPI) and the worker. They communicate through
RabbitMQ.

## Run it locally

Prerequisites:

- Python 3.12 or later and [`uv`](https://docs.astral.sh/uv/)
- A RabbitMQ server
- AWS credentials that `boto3` can find, with access to the S3 bucket and to SES

1. Install the dependencies:

   ```
   make setup
   ```

2. Set the environment variables. The gateway needs `QUEUE_URL`. The worker needs all four.

   | Variable | Used for |
   |---|---|
   | `QUEUE_URL` | AMQP URL of the RabbitMQ server |
   | `EXPORT_BUCKET` | S3 bucket that stores the encrypted CSV files |
   | `EXPORT_KEY` | Fernet key that encrypts each file |
   | `MAIL_FROM` | SES sender address of the download-link email |

3. Start the gateway on port 8080:

   ```
   make run-gateway
   ```

4. In a second terminal, start the worker:

   ```
   make run-worker
   ```

5. In a third terminal, request an export:

   ```
   curl -X POST localhost:8080/exports \
     -H 'Content-Type: application/json' \
     -d '{"account_id": "acme", "rows": 10}'
   ```

   The gateway answers `202` with `{"status":"queued"}`. The worker then uploads the file
   and emails `acme@accounts.example.com` a link.

The gateway rejects a request without `account_id` with `422`, and a request above
100,000 rows with `413`.

## How a job is processed

If the worker fails on a job, it puts the job back on the `exports` queue. After the
third failed attempt, it moves the job to the `exports.dead` queue. For the full flow, see
[docs/pipeline.md](docs/pipeline.md).

`deploy/alerts.yaml` defines a Prometheus alert, `ExportsDeadLetterHigh`, that pages when
`exports.dead` holds more than 10 messages for 5 minutes.

To move dead-lettered jobs back to `exports`, run the requeue script. Start with
`--dry-run`, which counts the messages and moves none:

```
uv run python scripts/requeue_dead.py --dry-run
uv run python scripts/requeue_dead.py --limit 50
```

`--limit` defaults to 100 messages. The script needs `QUEUE_URL`.

## Develop

Run the tests with:

```
make test
```
