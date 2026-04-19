# ---------- Builder ----------
FROM python:3.11.9-slim AS builder

WORKDIR /build

# Only copy requirements
COPY requirements.txt .

# Install deps into a virtual env
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---------- Runtime ----------
FROM python:3.11.9-slim

WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv

# Activate venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy app code
COPY . .

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "app.py"]