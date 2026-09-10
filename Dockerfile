FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=300

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

# CPU-only PyTorch
RUN pip install --no-cache-dir --no-compile \
    torch \
    --index-url https://download.pytorch.org/whl/cpu

# Application dependencies
RUN pip install --no-cache-dir --no-compile \
    -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "app.application"]