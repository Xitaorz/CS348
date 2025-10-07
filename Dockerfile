FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source and supporting assets
COPY src ./src
COPY schema.sql example.sql ./
# Copy default environment values; override at runtime as needed
COPY .env.example .env

EXPOSE 3000

CMD ["python", "-m", "src.app"]
