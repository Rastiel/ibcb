FROM python:3.11-slim

WORKDIR /usr/src/app

# requirements.txt'yi kopyala ve bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodları kopyala
COPY . .

# Uvicorn ile FastAPI’yi çalıştır
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
