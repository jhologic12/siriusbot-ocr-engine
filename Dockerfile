FROM python:3.12-slim

# ==================================
# Runtime environment
# ==================================

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_ENV=production


# ==================================
# System dependencies
# ==================================

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libgl1 \
    libmagic1 \
    curl \
    && rm -rf /var/lib/apt/lists/*


# ==================================
# Application directory
# ==================================

WORKDIR /app


# ==================================
# Python dependencies
# ==================================

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# ==================================
# Application source
# ==================================

COPY . .


# ==================================
# Security: non-root user
# ==================================

RUN useradd \
    --create-home \
    --shell /bin/bash \
    ocruser \
    && chown -R ocruser:ocruser /app


USER ocruser


# ==================================
# Service
# ==================================

EXPOSE 8000


# ==================================
# Container health
# ==================================

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=20s \
    --retries=3 \
    CMD curl --fail http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
