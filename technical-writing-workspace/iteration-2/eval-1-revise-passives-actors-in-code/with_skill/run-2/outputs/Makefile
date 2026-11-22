.PHONY: setup run-gateway run-worker test

setup:
	uv sync

run-gateway:
	uv run uvicorn exporter.gateway:app --port 8080

run-worker:
	uv run python -m exporter.worker

test:
	uv run pytest -q
