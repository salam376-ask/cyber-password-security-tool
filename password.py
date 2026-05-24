import re

weak_passwords = [
    "123456",
    "password",
    "admin",
    "qwerty",
    "12345678"
]

password = input("23e3: ")

score = 0

# Length scoring
if len(password) >= 8:
    score += 20
else:
    print("❌ Password should be at least 8 characters")

if len(password) >= 12:
    score += 10

# Uppercase
if re.search(r"[A-Z]", password):
    score += 20
else:
    print("❌ Add uppercase letters")

# Lowercase
if re.search(r"[a-z]", password):
    score += 20
else:
    print("❌ Add lowercase letters")

# Numbers
if re.search(r"[0-9]", password):
    score += 15
else:
    print("❌ Add numbers")

# Special characters
if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
    score += 15
else:
    print("❌ Add special characters")

# Weak password detection
if password.lower() in weak_passwords:
    print("❌ Very common password detected")
    score = 0

# Final Result
print(f"\nPassword Score: {score}/100")

if score >= 80:
    print("✅ Strong Password")

elif score >= 50:
    print("⚠ Medium Password")

else:
    print("❌ Weak Password")
