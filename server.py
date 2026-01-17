from flask import Flask, request
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

@app.route("/log", methods=["POST"])
def log():
    data = request.json
    msg = data.get("message", "LOG")

    requests.post(
        DISCORD_WEBHOOK,
        json={
            "username": "AutoSpace Logger",
            "content": msg
        }
    )
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
