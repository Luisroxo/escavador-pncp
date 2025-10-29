FROM python:3.11-slim
WORKDIR /app
COPY main.py .
RUN pip install fastapi requests psycopg2-binary uvicorn
EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]