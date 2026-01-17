from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

# ================== APP ==================
app = Flask(__name__)

# ================== ENV ==================
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
API_SECRET_KEY = os.environ.get("API_SECRET_KEY")

# ================== COLORS ==================
COLORS = {
    "SUCCESS": 0x2ecc71,
    "INFO": 0x3498db,
    "WARN": 0xf1c40f,
    "ERROR": 0xe74c3c
}

# ================== ROUTES ==================
@app.route("/")
def index():
    return "AutoSpace Logger API is running."

@app.route("/log", methods=["POST"])
def log():
    client_key = request.headers.get("X-API-KEY")

    # 🔒 GÜVENLİK KONTROLLERİ
    if not API_SECRET_KEY:
        return jsonify({"error": "server_not_configured"}), 500

    if not client_key:
        return jsonify({"error": "missing_api_key"}), 403

    if client_key != API_SECRET_KEY:
        return jsonify({"error": "invalid_api_key"}), 403

    data = request.json or {}
    level = data.get("level", "INFO")
    message = data.get("message", "")
    user = data.get("user", "UNKNOWN")

    embed = {
        "title": f"AutoSpace Log • {level}",
        "description": f"**Mesaj:** {message}\n**Kullanıcı:** {user}",
        "color": COLORS.get(level, 0x95a5a6),
        "footer": {
            "text": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    requests.post(
        DISCORD_WEBHOOK,
        json={
            "username": "AutoSpace",
            "embeds": [embed]
        },
        timeout=5
    )

    return jsonify({"status": "ok"}), 200


# ================== START ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
