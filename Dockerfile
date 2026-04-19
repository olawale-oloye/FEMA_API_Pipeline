# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy ONLY requirements first (for caching)
COPY requirements.txt .


# Install dependencies
RUN python -m pip install --upgrade pip \
&&  python -m pip install --no-cache-dir -r requirements.txt


# Copy files
COPY . .

# Create non-root user
RUN useradd -m appuser
USER appuser

# Environment
ENV PYTHONUNBUFFERED=1

# Run app
CMD ["python", "app.py"]