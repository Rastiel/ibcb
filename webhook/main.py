import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# .env dosyasını yükle
load_dotenv()

# Ortam değişkenlerini oku
DB_HOST      = os.getenv("DB_HOST")
DB_USER      = os.getenv("DB_USER")
DB_PASS      = os.getenv("DB_PASS")
DB_NAME      = os.getenv("DB_NAME")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# SQLAlchemy ayarları
DB_URL       = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine       = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def verify():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/", methods=["POST"])
def webhook():
    # Gelen JSON payload'u al
    data = request.get_json()

    # → İşte eklenen satır: tüm veriyi console'a basıyoruz
    print("Incoming webhook data:", data)

    # Mesaj işleme ve DB kaydı
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

                session = SessionLocal()
                try:
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
    # Geliştirme modunda doğrudan flask ile çalıştırmak için
    app.run(host="0.0.0.0", port=5000)
