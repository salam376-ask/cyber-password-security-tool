import re
import random
import string
import tkinter as tk
from datetime import datetime
from cryptography.fernet import Fernet

# LOAD KEY
with open("secret.key", "rb") as f:
    key = f.read()

cipher = Fernet(key)

weak_passwords = ["123456", "password", "admin", "qwerty", "12345678"]


# ENCRYPT SAVE
def save_password(password, score):
    data = f"{datetime.now()} | {password} | Score: {score}/100"
    encrypted = cipher.encrypt(data.encode())

    with open("password_history.enc", "ab") as f:
        f.write(encrypted + b"\n")


# DECRYPT HISTORY
def view_history():
    try:
        with open("password_history.enc", "rb") as f:
            lines = f.readlines()

        decrypted_data = []

        for line in lines:
            try:
                decrypted = cipher.decrypt(line.strip()).decode()
                decrypted_data.append(decrypted)
            except:
                decrypted_data.append("[ERROR DECODING ENTRY]")

    except:
        decrypted_data = ["No history found"]

    window = tk.Toplevel(app)
    window.title("Encrypted Password History")
    window.geometry("500x300")

    text = tk.Text(window)
    text.pack(expand=True, fill="both")

    text.insert("end", "\n".join(decrypted_data))


# CHECK PASSWORD
def check_password():
    password = password_entry.get()

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 20
    else:
        feedback.append("• At least 8 characters")

    if len(password) >= 12:
        score += 10

    if re.search(r"[A-Z]", password):
        score += 20
    else:
        feedback.append("• Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 20
    else:
        feedback.append("• Add lowercase letters")

    if re.search(r"[0-9]", password):
        score += 15
    else:
        feedback.append("• Add numbers")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 15
    else:
        feedback.append("• Add special characters")

    if password.lower() in weak_passwords:
        score = 0
        feedback.append("• Very common password")

    if score >= 80:
        result = "✅ STRONG PASSWORD"
    elif score >= 50:
        result = "⚠ MEDIUM PASSWORD"
    else:
        result = "❌ WEAK PASSWORD"

    output_label.config(
        text=f"{result}\nScore: {score}/100\n\n" + "\n".join(feedback)
    )

    save_password(password, score)


# GENERATE PASSWORD
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    generated = ''.join(random.choice(chars) for _ in range(16))

    password_entry.delete(0, tk.END)
    password_entry.insert(0, generated)


# GUI
app = tk.Tk()
app.title("Cyber Password Tool v8 (Encrypted)")
app.geometry("520x450")
app.configure(bg="black")

title = tk.Label(app, text="ENCRYPTED PASSWORD TOOL",
                  fg="lime", bg="black", font=("Arial", 16, "bold"))
title.pack(pady=10)

password_entry = tk.Entry(app, width=35, bg="#111", fg="lime",
                          insertbackground="lime", show="*")
password_entry.pack(pady=10)

tk.Button(app, text="Check Password", command=check_password,
          bg="#111", fg="lime", width=25).pack(pady=3)

tk.Button(app, text="Generate Password", command=generate_password,
          bg="#111", fg="lime", width=25).pack(pady=3)

tk.Button(app, text="View Encrypted History", command=view_history,
          bg="#111", fg="lime", width=25).pack(pady=3)

output_label = tk.Label(app, text="", fg="lime", bg="black", justify="left")
output_label.pack(pady=10)

app.mainloop()
