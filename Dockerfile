FROM python:3.11-slim

WORKDIR /todo

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY routers/ ./routers/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]