import os
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# .env içindeki değişkenleri yükle
load_dotenv()

# Veritabanı bağlantı URL'sini oluştur
DB_URL = (
    f"mysql+mysqlconnector://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)

# SQLAlchemy engine ve session fabrikasını hazırla
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI uygulamasını başlat
app = FastAPI()

@app.get("/health")
def health():
    """
    Sağlık kontrol endpoint’i.
    Docker Compose aracılığıyla ayağa kalktıktan sonra
    bu endpoint’e istek atarak servis durumunu görebilirsin.
    """
    return {"status": "ok"}

# TODO: Bot mantığı için diğer endpoint’leri buraya ekle

# Eğer dosya doğrudan çalıştırılırsa Uvicorn ile başlat
if __name__ == "__main__":
    import uvicorn
    # Uygulamayı 0.0.0.0:8000 üzerinde ayağa kaldır
    uvicorn.run(app, host="0.0.0.0", port=8000)
