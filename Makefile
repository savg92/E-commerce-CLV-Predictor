.PHONY: setup test lint

setup:
	uv sync
	bun install

test:
	uv run pytest --cov=packages/backend/src --cov-report=term-missing
	bun run --cwd packages/frontend test

lint:
	uv run ruff check packages/backend/src || true
	bun run --cwd packages/frontend lint
