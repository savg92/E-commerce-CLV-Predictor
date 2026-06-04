FROM python:3.10-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
COPY packages/backend/pyproject.toml ./packages/backend/
COPY packages/backend/src ./packages/backend/src

# Use CPU-only torch
ENV PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu

RUN uv sync --no-dev --package backend

FROM python:3.10-slim AS runner
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
# Copy only the necessary source code
COPY packages/backend/src /app/packages/backend/src
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/packages/backend/src"

# Final cleanup
RUN find /app/.venv -name "__pycache__" -exec rm -rf {} + && \
    find /app/.venv -name "*.pyc" -exec rm -f {} +

CMD ["uvicorn", "backend.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
