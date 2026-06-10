.PHONY: setup test lint docker-build docker-up doc-lint dev-backend dev-frontend dev

setup:
	uv sync
	bun install

dev:
	make -j 2 dev-backend dev-frontend

dev-backend:
	PYTHONPATH=packages/backend/src uv run uvicorn backend.api.app:app --reload --port 8000

dev-frontend:
	bun run --cwd packages/frontend dev

test:
	uv run pytest --cov=packages/backend/src --cov-report=term-missing
	bun run --cwd packages/frontend test

lint:
	uv run ruff check packages/backend/src || true
	bun run --cwd packages/frontend lint

doc-lint:
	# Simple check: verify no empty headers in markdown files
	! grep -r --exclude-dir=node_modules "^# [[:space:]]*$$" docs/ README.md
	# Verify internal links
	grep -ro --exclude-dir=node_modules --exclude-dir=.venv --exclude-dir=.git --exclude-dir=.pytest_cache "\[.*\](docs/[^)]*\.md)" . | while read -r line; do \
		file=$$(echo $$line | cut -d':' -f2 | cut -d'(' -f2 | cut -d')' -f1); \
		if [ ! -f "$$file" ]; then echo "Broken link: $$file"; exit 1; fi; \
	done


docker-build:
	docker-compose build

docker-up:
	docker-compose up
