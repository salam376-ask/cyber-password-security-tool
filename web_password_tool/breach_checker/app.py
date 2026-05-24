from flask import Flask, request

app = Flask(__name__)

# LOAD BREACHED PASSWORDS
def load_breaches():
    try:
        with open("breached.txt", "r") as f:
            return set(line.strip() for line in f)
    except:
        return set()

breached_passwords = load_breaches()


def check_password(password):

    if password.lower() in breached_passwords:
        return "❌ BREACHED PASSWORD (HIGH RISK)"

    return "✅ NOT FOUND IN BREACH LIST (LOW RISK)"


@app.route("/", methods=["GET", "POST"])
def index():

    result = ""

    if request.method == "POST":
        password = request.form["password"]
        result = check_password(password)

    return f"""
    <html>
    <head>
        <title>Breach Password Checker</title>
        <style>
            body {{
                background: black;
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
        <h1>BREACH PASSWORD CHECKER</h1>

        <form method="POST">
            <input type="text" name="password" placeholder="Enter password">
            <button type="submit">Check</button>
        </form>

        <h2>{result}</h2>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
