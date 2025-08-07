FROM python:3.10-slim
WORKDIR /app
COPY backend/ /app/
COPY db/ /app/db/
COPY models/ /app/models/
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]