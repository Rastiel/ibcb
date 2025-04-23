import os
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. .env’deki DB ayarlarını yükle
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# 2. SQLAlchemy bağlantısını kur
DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. FastAPI uygulamasını başlat
app = FastAPI()

@app.get("/health")
def health():
    """
    Health check endpoint’i.
    Servisin ayağa kalkıp kalkmadığını test etmek için kullan.
    """
    return {"status": "ok"}

# TODO: Bot iş mantığı endpoint’lerini buraya ekle

if __name__ == "__main__":
    # doğrudan python main.py ile test etmek için
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
