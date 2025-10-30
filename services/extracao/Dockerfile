FROM python:3.11-slim-bullseye
WORKDIR /app
COPY main.py .
RUN apt-get update && apt-get install -y iputils-ping && pip install --upgrade pip && pip install fastapi pdfplumber uvicorn python-multipart prometheus_fastapi_instrumentator
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]