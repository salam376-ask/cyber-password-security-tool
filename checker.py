import re

weak_passwords = [
    "123456",
    "password",
    "admin",
    "qwerty",
    "12345678"
]

password = input("pretty: ")

score = 0

# Length check
if len(password) >= 8:
    score += 1
else:
    print("❌ Password should be at least 8 characters")

# Uppercase check
if re.search(r"[A-Z]", password):
    score += 1
else:
    print("❌ Add uppercase letters")

# Lowercase check
if re.search(r"[a-z]", password):
    score += 1
else:
    print("❌ Add lowercase letters")

# Number check
if re.search(r"[0-9]", password):
    score += 1
else:
    print("❌ Add numbers")

# Special character check
if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
    score += 1
else:
    print("❌ Add special characters")

# Weak password check
if password.lower() in weak_passwords:
    print("❌ Very common password detected")
    score = 0

# Final result
print("\nPassword Strength Result:")

if score == 5:
    print("✅ Strong Password")

elif score >= 3:
    print("⚠ Medium Password")

else:
    print("❌ Weak Password")
