# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Copy only necessary files
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure scripts are executable
RUN chmod +x /app/scripts/*.sh

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860')"

# Metadata
LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="Agno Documentation Crawler"

ENTRYPOINT ["python", "crawl_docs.py"]