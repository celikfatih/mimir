FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Set PYTHONPATH to include src
ENV PYTHONPATH=/app

CMD ["python", "-m", "src.mimir_syncer.main"]
