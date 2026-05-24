from flask import Flask, request, jsonify
import json
from datetime import datetime
import requests

app = Flask(__name__)

LOG_FILE = "logs.json"


# -------------------------
# LOG SYSTEM
# -------------------------
def log_event(source, event, level):

    log = {
        "time": str(datetime.now()),
        "source": source,
        "event": event,
        "level": level
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(log)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------
# API ENDPOINT (REAL SOC INTAKE)
# -------------------------
@app.route("/log", methods=["POST"])
def receive_log():

    data = request.json

    source = data.get("source")
    event = data.get("event")
    level = data.get("level")

    log_event(source, event, level)

    return jsonify({"status": "logged"})


# -------------------------
# DASHBOARD
# -------------------------
@app.route("/")
def dashboard():

    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    html = """
    <html>
    <head>
        <title>SOC PRO LIVE SYSTEM</title>
        <style>
            body { background:black; color:lime; font-family:Arial; }
            table { width:85%; margin:auto; border:1px solid lime; }
            th, td { border:1px solid lime; padding:8px; }
        </style>
    </head>

    <body>
        <h1 style="text-align:center;">SOC PRO LIVE DASHBOARD</h1>

        <table>
        <tr>
            <th>Time</th>
            <th>Source</th>
            <th>Event</th>
            <th>Level</th>
        </tr>
    """

    for log in logs[::-1]:
        html += f"""
        <tr>
            <td>{log['time']}</td>
            <td>{log['source']}</td>
            <td>{log['event']}</td>
            <td>{log['level']}</td>
        </tr>
        """

    html += "</table></body></html>"

    return html


# -------------------------
# SIMULATED MODULES
# -------------------------
def run_port_scanner():
    data = {
        "source": "PORT SCANNER",
        "event": "SSH port 22 open detected",
        "level": "HIGH"
    }
    requests.post("http://127.0.0.1:5000/log", json=data)


def run_password_tool():
    data = {
        "source": "PASSWORD TOOL",
        "event": "Weak password detected (admin123)",
        "level": "MEDIUM"
    }
    requests.post("http://127.0.0.1:5000/log", json=data)


def run_breach_checker():
    data = {
        "source": "BREACH CHECKER",
        "event": "Password found in leaked database",
        "level": "CRITICAL"
    }
    requests.post("http://127.0.0.1:5000/log", json=data)


# -------------------------
# AUTO TEST (runs once on start)
# -------------------------
def generate_demo_logs():
    run_port_scanner()
    run_password_tool()
    run_breach_checker()


# -------------------------
# START SERVER
# -------------------------
if __name__ == "__main__":
    generate_demo_logs()
    app.run(debug=True)
