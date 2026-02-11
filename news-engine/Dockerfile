# Use slim Python image for system deps support
FROM python:3.12-slim

WORKDIR /app

# Install system deps for psycopg2, Pillow, numpy, pandas, etc.
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Build wheels inside container and install
RUN pip install --no-cache-dir wheel \
    && pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt \
    && pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy rest of project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn (without --reload for production)
# Use --reload only in development via docker-compose override
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
