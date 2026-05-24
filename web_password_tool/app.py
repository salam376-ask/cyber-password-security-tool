from flask import Flask, request

app = Flask(__name__)

import re
import random
import string

weak_passwords = ["123456", "password", "admin", "qwerty", "12345678"]


def check_strength(password):

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 20
    else:
        feedback.append("At least 8 characters")

    if len(password) >= 12:
        score += 10

    if re.search(r"[A-Z]", password):
        score += 20
    else:
        feedback.append("Add uppercase")

    if re.search(r"[a-z]", password):
        score += 20
    else:
        feedback.append("Add lowercase")

    if re.search(r"[0-9]", password):
        score += 15
    else:
        feedback.append("Add numbers")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 15
    else:
        feedback.append("Add special chars")

    if password.lower() in weak_passwords:
        score = 0
        feedback.append("Very common password")

    if score >= 80:
        result = "STRONG"
    elif score >= 50:
        result = "MEDIUM"
    else:
        result = "WEAK"

    return result, score, feedback


def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(16))


@app.route("/", methods=["GET", "POST"])
def index():

    result = ""
    score = ""
    feedback = []
    generated = ""

    if request.method == "POST":

        if "check" in request.form:
            password = request.form["password"]
            result, score, feedback = check_strength(password)

        if "generate" in request.form:
            generated = generate_password()

    return f"""
    <html>
    <head>
        <title>Cyber Password Tool</title>
        <style>
            body {{
                background-color: black;
                color: lime;
                font-family: Arial;
                text-align: center;
            }}
            input, button {{
                padding: 10px;
                margin: 5px;
            }}
        </style>
    </head>

    <body>
        <h1>CYBER PASSWORD SECURITY TOOL</h1>

        <form method="POST">
            <input type="text" name="password" placeholder="Enter password">
            <br>
            <button name="check">Check Password</button>
            <button name="generate">Generate Password</button>
        </form>

        <h2>Result: {result}</h2>
        <h3>Score: {score}</h3>

        <p>{"<br>".join(feedback)}</p>

        <h2>Generated Password:</h2>
        <p>{generated}</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
