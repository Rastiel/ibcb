# Base image olarak hafif ve güncel bir Python sürümü kullanıyoruz
FROM python:3.11-slim

# Çalışma dizinini belirliyoruz
WORKDIR /usr/src/app

# Önce sadece requirements.txt’i kopyalayıp bağımlılıkları yüklüyoruz
# Böylece kod değişmediğinde layer cache’den yararlanırız
COPY requirements.txt .

# Bağımlılıkları --no-cache-dir ile yükleyerek imajı hafif tutuyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu konteynıra kopyala
COPY . .

# Container ayağa kalkarken Uvicorn ile FastAPI uygulamasını sun
# --host 0.0.0.0: tüm arayüzlerden erişime aç
# --port 8000: api endpoint’imizin dinleyeceği port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
