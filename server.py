from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

COLORS = {
    "SUCCESS": 0x2ecc71,
    "INFO": 0x3498db,
    "WARN": 0xf1c40f,
    "ERROR": 0xe74c3c
}

@app.route("/log", methods=["POST"])
def log():
    data = request.json
    message = data.get("message", "")
    
    # Mesajdan level ve kullanıcıyı ayıkla
    # Format: [LEVEL] mesaj | Kullanıcı | saat
    try:
        level = message.split("]")[0].replace("[", "")
    except:
        level = "INFO"

    embed = {
        "title": f"AutoSpace Log • {level}",
        "description": message,
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
        }
    )

    return {"status": "ok"}

app.run(host="0.0.0.0", port=10000)
