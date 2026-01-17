@app.route("/log", methods=["POST"])
def log():
    client_key = request.headers.get("X-API-KEY")

    # 🔐 MUTLAK KONTROL
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
