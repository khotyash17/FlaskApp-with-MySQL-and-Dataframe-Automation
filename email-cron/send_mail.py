import os
import sys
import mysql.connector
import pandas as pd
import msoffcrypto
import io
import yagmail
from datetime import datetime

# Environment variables
OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
EMAIL_PASS = os.environ.get("OWNER_PASS")
TO_EMAIL = os.environ.get("TO_EMAIL")
XLS_PASS = os.environ.get("XLS_PASS")

if not OWNER_EMAIL or not EMAIL_PASS or not TO_EMAIL:
    print("❌ OWNER_EMAIL, OWNER_PASS, or TO_EMAIL not set in environment")
    sys.exit(1)

EXPORT_DIR = "/app/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

# Generate Excel from DB
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#xlsx_file = f"{EXPORT_DIR}/students_{timestamp}.xlsx"
secure_xlsx_file = f"{EXPORT_DIR}/students_{timestamp}_secure.xlsx"

conn = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "db"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASS", "password"),
    database=os.environ.get("DB_NAME", "studentsdb")
)
df = pd.read_sql("SELECT * FROM students;", conn)
conn.close()

df.to_excel(secure_xlsx_file, index=False)
print(f"✅ Excel created: {secure_xlsx_file}")

# Encrypt Excel with password
with open(secure_xlsx_file, "rb") as f_in:
    office_file = msoffcrypto.OfficeFile(f_in)
    with open(secure_xlsx_file, "wb") as f_out:
        office_file.encrypt(XLS_PASS, f_out)

print(f"🔒 Password-protected Excel created: {secure_xlsx_file}")

# Send email
try:
    yag = yagmail.SMTP(OWNER_EMAIL, EMAIL_PASS)
    yag.send(
        to=TO_EMAIL,
        subject="Secure Student Excel",
        contents=f"Hi,\n\nAttached is the password-protected Excel file.\nPassword: {XLS_PASS}\n\nRegards",
        attachments=secure_xlsx_file
    )
    print(f"📩 Sent {secure_xlsx_file} to {TO_EMAIL}")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
