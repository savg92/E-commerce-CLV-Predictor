.PHONY: setup test lint docker-build docker-up doc-lint

setup:
	uv sync
	bun install

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
	grep -ro --exclude-dir=node_modules "\[.*\](docs/[^)]*\.md)" . | while read -r line; do \
		file=$$(echo $$line | cut -d':' -f2 | cut -d'(' -f2 | cut -d')' -f1); \
		if [ ! -f "$$file" ]; then echo "Broken link: $$file"; exit 1; fi; \
	done

docker-build:
	docker-compose build

docker-up:
	docker-compose up
