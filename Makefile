.PHONY: setup test lint docker-build docker-up

setup:
	uv sync
	bun install

test:
	uv run pytest --cov=packages/backend/src --cov-report=term-missing
	bun run --cwd packages/frontend test

lint:
	uv run ruff check packages/backend/src || true
	bun run --cwd packages/frontend lint

docker-build:
	docker-compose build

docker-up:
	docker-compose up
