import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()

# Ortam değişkenleri
DB_HOST      = os.getenv("DB_HOST")
DB_USER      = os.getenv("DB_USER")
DB_PASS      = os.getenv("DB_PASS")
DB_NAME      = os.getenv("DB_NAME")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
IG_APP_ID    = os.getenv("IG_APP_ID")
IG_TOKEN     = os.getenv("IG_ACCESS_TOKEN")

# DB ayarları
DB_URL       = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine       = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)

def send_reply(to_id: str, text: str):
    """
    Instagram Graph API üzerinden yanıt gönderir.
    """
    url = f"https://graph.facebook.com/v17.0/{IG_APP_ID}/messages"
    headers = {"Authorization": f"Bearer {IG_TOKEN}"}
    payload = {
        "messaging_product": "instagram",
        "to": to_id,
        "text": {"body": text}
    }
    resp = requests.post(url, json=payload, headers=headers)
    if not resp.ok:
        print("Reply failed:", resp.status_code, resp.text)
    return resp.json()

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
    data = request.get_json()
    print("Incoming webhook data:", data)

    entries = data.get("entry", [])
    for entry in entries:
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for msg in value.get("messages", []):
                user_id = msg.get("from")
                text    = msg.get("text", {}).get("body", "")
                ts      = datetime.fromtimestamp(int(msg.get("timestamp", 0)))

                # DB kaydı
                session = SessionLocal()
                try:
                    from app.models import Message
                    db_msg = Message(
                        id=int(msg["id"], 36),
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

                # Otomatik cevap
                reply_text = f"Merhaba! Mesajını aldım: \"{text}\""
                send_reply(user_id, reply_text)

    return jsonify(success=True), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
