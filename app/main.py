import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 1. .env içindeki tüm değişkenleri yükle
load_dotenv()

# 2. Ortam değişkenlerini oku
DB_HOST      = os.getenv("DB_HOST")
DB_USER      = os.getenv("DB_USER")
DB_PASS      = os.getenv("DB_PASS")
DB_NAME      = os.getenv("DB_NAME")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# 3. SQLAlchemy engine ve session fabrikası oluştur
DB_URL       = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine       = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)

@app.route("/webhook/", methods=["GET"])
def verify():
    """
    Webhook doğrulama endpoint’i.
    Meta’dan gelen GET isteğinde hub.verify_token ile .env’deki VERIFY_TOKEN eşleşirse
    hub.challenge değerini döner; aksi halde 403 hatası verir.
    """
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook/", methods=["POST"])
def webhook():
    """
    Asıl webhook handler.
    Gelen JSON payload’u alır, mesaj bilgilerini parse eder,
    SQLAlchemy üzerinden MySQL’e kaydeder ve 200 OK döner.
    """
    data = request.get_json()
    print("Incoming webhook data:", data)

    # Örnek: Entry içinden ilk mesajı çek
    entries = data.get("entry", [])
    if entries:
        changes = entries[0].get("changes", [])
        if changes:
            value    = changes[0].get("value", {})
            messages = value.get("messages", [])
            if messages:
                msg       = messages[0]
                user_id   = msg.get("from")
                text      = msg.get("text", {}).get("body", "")
                ts_unix   = int(msg.get("timestamp", 0))
                ts        = datetime.fromtimestamp(ts_unix)

                # Veritabanına kaydet
                session = SessionLocal()
                try:
                    # app/models.py içindeki Message modelini kullanıyoruz
                    from app.models import Message
                    db_msg = Message(
                        id=int(msg["id"], 36) if msg.get("id") else None,
                        user_id=int(user_id),
                        direction="in",
                        text=text,
                        timestamp=ts
                    )
                    session.add(db_msg)
                    session.commit()
                    print(f"Saved message from {user_id}: {text}")
                except Exception as e:
                    session.rollback()
                    print("Error saving message:", e)
                finally:
                    session.close()

    return jsonify(success=True), 200

if __name__ == "__main__":
    """
    Geliştirme sırasında doğrudan python main.py
    komutuyla da test edebilmek için app.run ekliyoruz.
    """
    app.run(host="0.0.0.0", port=5000)
