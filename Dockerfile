# Base Python image
FROM python:3.10-slim

# Python environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Working directory inside container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install CPU-only PyTorch
RUN pip install --no-cache-dir --timeout 300 \
    torch \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining Python dependencies
RUN pip install --no-cache-dir --timeout 300 \
    -r requirements.txt

# Copy project files
COPY . .

# Flask application port
EXPOSE 5000

# Start Flask application
CMD ["python", "app/application.py"]