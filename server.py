from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Discord webhook (Render Environment Variable)
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# Embed renkleri
COLORS = {
    "SUCCESS": 0x2ecc71,  # Yeşil
    "INFO": 0x3498db,     # Mavi
    "WARN": 0xf1c40f,     # Sarı
    "ERROR": 0xe74c3c     # Kırmızı
}

@app.route("/log", methods=["POST"])
def log():
    data = request.json or {}

    level = data.get("level", "INFO")
    message = data.get("message", "")
    user = data.get("user", "Bilinmeyen")

    embed = {
        "title": f"AutoSpace Log • {level}",
        "description": f"**Mesaj:** {message}\n**Kullanıcı:** {user}",
        "color": COLORS.get(level, 0x95a5a6),
        "footer": {
            "text": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    try:
        requests.post(
            DISCORD_WEBHOOK,
            json={
                "username": "AutoSpace",
                "embeds": [embed]
            },
            timeout=5
        )
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

    return jsonify({"status": "ok"}), 200


@app.route("/", methods=["GET"])
def index():
    return "AutoSpace Logger API is running.", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
