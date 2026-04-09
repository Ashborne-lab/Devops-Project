# ── Stage 1: Build ────────────────────────────────────────────────────────
FROM python:3.9-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Runtime ─────────────────────────────────────────────────────
FROM python:3.9-slim

LABEL maintainer="devops-team"
LABEL version="2.0.0"
LABEL description="Production telemetry Flask application"

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy only the installed deps from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app.py .
COPY templates/ templates/

# Own everything by the non-root user
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "app.py"]