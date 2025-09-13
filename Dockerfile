# Base image
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base AS dev

# Install dev utilities (like ping)
RUN apt-get update && apt-get install -y iputils-ping

# Copy project files
COPY . .

# Run Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
