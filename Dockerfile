FROM python:3.11-slim

WORKDIR /todo

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

ENV TODO_DATA_FILE=/data/todo_data.json

CMD uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4 --root-path "${ROOT_PATH}"