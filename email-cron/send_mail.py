import sys
import os
import yagmail

OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
OWNER_PASS = os.environ.get("OWNER_PASS")
TO_EMAIL = os.environ.get("TO_EMAIL")

if not OWNER_EMAIL or not OWNER_PASS or not TO_EMAIL:
    print("❌ Missing OWNER_EMAIL, OWNER_PASS, or TO_EMAIL in environment")
    sys.exit(1)

if len(sys.argv) < 2:
    print("❌ No file passed to send_mail.py")
    sys.exit(1)

file_to_send = sys.argv[1]

if not os.path.exists(file_to_send):
    print(f"❌ File not found: {file_to_send}")
    sys.exit(1)

try:
    yag = yagmail.SMTP(user=OWNER_EMAIL, password=OWNER_PASS)
    yag.send(
        to=TO_EMAIL,
        subject="🔒 Encrypted Student Report",
        contents="Hi,\n\nPlease find attached your password-protected student report.\nPassword: use the one you set in .env",
        attachments=file_to_send
    )
    print(f"✅ Sent {file_to_send} to {TO_EMAIL}")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
