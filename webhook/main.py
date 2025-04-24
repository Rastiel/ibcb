import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/webhook/", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == os.getenv("VERIFY_TOKEN"):
        return challenge, 200
    return "Verification failed", 403

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)
    # TODO: handle incoming messages and save to DB
    return jsonify(success=True), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
