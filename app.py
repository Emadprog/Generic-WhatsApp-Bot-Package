from flask import Flask, request, Response, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

# =============================
# Load Config
# =============================
def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

# =============================
# Log Incoming Messages
# =============================
def log_message(sender, message):
    os.makedirs("logs", exist_ok=True)
    with open("logs/messages.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {sender} : {message}\n")


# =============================
# Webhook Route (Twilio)
# =============================
@app.route("/webhook", methods=["POST"])
def webhook():
    cfg = load_config()
    data = request.form
    sender = data.get("From", "")
    message = data.get("Body", "").strip()

    log_message(sender, message)

    responses = cfg.get("responses", {})

    reply = None
    for keyword, response_text in responses.items():
        if keyword.lower() in message.lower():
            reply = response_text
            break

    if not reply:
        reply = cfg.get("fallback_message", "Sorry, I didn't understand.")

    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

    return Response(xml_response, mimetype="application/xml")


# =============================
# Dashboard: Show Logs
# =============================
@app.route("/dashboard/messages")
def dashboard_messages():
    log_path = os.path.join("logs", "messages.log")

    if not os.path.exists(log_path):
        logs = "No messages received yet."
    else:
        with open(log_path, "r", encoding="utf-8") as f:
            logs = f.read()

    html_path = os.path.join("dashboard", "messages.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    return render_template_string(html_template, logs=logs)

# =============================
# Dashboard: Edit Responses
# =============================
@app.route("/dashboard/settings", methods=["GET", "POST"])
def dashboard_settings():
    config_path = "config.json"

    # ========== لو المستخدم حفظ التعديلات ==========
    if request.method == "POST":
        new_config_text = request.form.get("config_text")

        try:
            # التأكد إن JSON صحيح
            new_json = json.loads(new_config_text)

            # كتابة التعديلات داخل config.json
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(new_json, f, indent=4, ensure_ascii=False)

            return "<h2>✅ Saved!</h2><a href='/dashboard/settings'>Back</a>"

        except Exception as e:
            return f"<h2>❌ JSON ERROR:</h2><pre>{e}</pre><a href='/dashboard/settings'>Back</a>"

    # ========== GET - أول مرة يفتح الصفحة ==========
    with open(config_path, "r", encoding="utf-8") as f:
        config_text = f.read()

    html_path = os.path.join("dashboard", "settings.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    return render_template_string(html_template, config_text=config_text)
# =============================
# Dashboard: Restart Bot
# =============================
@app.route("/dashboard/restart", methods=["GET", "POST"])
def dashboard_restart():
    html_path = os.path.join("dashboard", "restart.html")

    # GET → عرض صفحة الزر
    if request.method == "GET":
        with open(html_path, "r", encoding="utf-8") as f:
            return render_template_string(f.read())

    # POST → تنفيذ Restart
    if request.method == "POST":
        # ✅ كتابة علامة إعادة التشغيل
        with open("restart.flag", "w") as f:
            f.write("restart")
# =============================
# Dashboard: Home Page
# =============================
@app.route("/dashboard")
def dashboard_home():
    html_path = os.path.join("dashboard", "home.html")

    with open(html_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    return render_template_string(html_template)

    return "<h2>✅ Bot Restarted Successfully!</h2><a href='/dashboard/restart'>Back</a>"
    return render_template_string(html_template, config_text=config_text)
# =============================
# Run Server
# =============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
