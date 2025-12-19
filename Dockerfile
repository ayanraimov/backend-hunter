# Multi-stage build for smaller final image
FROM python:3.13-slim as builder

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Export requirements (sin dev dependencies)
RUN poetry export -f requirements.txt --without-hashes --only main > requirements.txt

# Final stage
FROM python:3.13-slim

WORKDIR /app

# Install dependencies from requirements.txt
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose API port
EXPOSE 8000

# Default command: run the API
CMD ["uvicorn", "src.backend_hunter.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
