FROM python:3.10-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
COPY packages/backend/pyproject.toml ./packages/backend/
RUN uv sync --no-dev --package backend

FROM python:3.10-slim AS runner
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/packages/backend/src"
CMD ["uvicorn", "backend.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
