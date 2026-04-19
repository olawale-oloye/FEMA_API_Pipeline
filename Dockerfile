FROM python:3.11.9-slim

WORKDIR /app

# Install dependencies first
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create non-root user
RUN useradd -m appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "app.py"]