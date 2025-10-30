FROM python:3.11-slim-bullseye
WORKDIR /app
COPY main.py .
RUN apt-get update && apt-get install -y iputils-ping curl && pip install --upgrade pip && pip install fastapi requests psycopg2-binary uvicorn prometheus_fastapi_instrumentator
EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]