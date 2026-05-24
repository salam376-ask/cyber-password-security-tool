from flask import Flask, request
import json
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "logs.json"


# SAVE LOGS
def save_log(ip, event, level):

    log = {
        "time": str(datetime.now()),
        "ip": ip,
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


# DETECTION ENGINE
def analyze(ip, event):

    event = event.lower()

    if "failed login" in event:
        return "HIGH"

    elif "port scan" in event:
        return "MEDIUM"

    elif "login success" in event:
        return "LOW"

    return "INFO"


@app.route("/", methods=["GET", "POST"])
def dashboard():

    message = ""

    if request.method == "POST":

        ip = request.form["ip"]
        event = request.form["event"]

        level = analyze(ip, event)
        save_log(ip, event, level)

        message = f"Logged Event → {level} Risk"

    # LOAD LOGS
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    html = """
    <html>
    <head>
        <title>Mini SIEM</title>
        <style>
            body { background:black; color:lime; font-family:Arial; }
            table { width:80%; margin:auto; border:1px solid lime; }
            th, td { border:1px solid lime; padding:8px; }
        </style>
    </head>

    <body>
        <h1 style="text-align:center;">MINI SIEM DASHBOARD</h1>

        <form method="POST" style="text-align:center;">
            <input name="ip" placeholder="IP Address">
            <input name="event" placeholder="Event (login, scan, etc)">
            <button type="submit">Add Event</button>
        </form>

        <h3 style="text-align:center;">{message}</h3>

        <h2 style="text-align:center;">LOGS</h2>

        <table>
            <tr>
                <th>Time</th>
                <th>IP</th>
                <th>Event</th>
                <th>Risk</th>
            </tr>
    """

    for log in logs[::-1]:
        html += f"""
        <tr>
            <td>{log['time']}</td>
            <td>{log['ip']}</td>
            <td>{log['event']}</td>
            <td>{log['level']}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(debug=True)
