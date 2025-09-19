import os
import sys
import pandas as pd
import pymysql
import datetime
import msoffcrypto
import yagmail

# Environment variables
OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
EMAIL_PASS = os.environ.get("OWNER_PASS")
TO_EMAIL = os.environ.get("TO_EMAIL")
XLS_PASS = os.environ.get("XLS_PASS")

if not OWNER_EMAIL or not EMAIL_PASS or not TO_EMAIL or not XLS_PASS:
    print("❌ OWNER_EMAIL, EMAIL_PASS, TO_EMAIL or XLS_PASS not set in environment")
    sys.exit(1)

EXPORT_DIR = "/app/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

# Connect to DB
conn = pymysql.connect(
    host=os.environ.get("DB_HOST", "mysql-db"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASS", "password"),
    database=os.environ.get("DB_NAME", "studentsdb")
)

# Fetch data
df = pd.read_sql("SELECT * FROM students;", conn)
conn.close()

# Create plain Excel file first
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
plain_file = f"{EXPORT_DIR}/students_{timestamp}_plain.xlsx"
df.to_excel(plain_file, index=False)
print(f"✅ Plain Excel created: {plain_file}")

# Encrypt Excel with password
secure_file = f"{EXPORT_DIR}/students_{timestamp}.xlsx"
with open(plain_file, "rb") as f_in, open(secure_file, "wb") as f_out:
    office_file = msoffcrypto.OfficeFile(f_in)
    office_file.encrypt(XLS_PASS, f_out)  # pass both password and output file

os.remove(plain_file)  # remove unprotected file
print(f"🔒 Password-protected Excel created: {secure_file}")

# Send email with attachment
try:
    yag = yagmail.SMTP(OWNER_EMAIL, EMAIL_PASS)
    yag.send(
        to=TO_EMAIL,
        subject="Secure Student Excel",
        contents=f"""
Hi,

Please find attached the student list in Excel.
🔑 Password to open file: {XLS_PASS}

Regards,
Automation Script
""",
        attachments=secure_file
    )
    print(f"📩 Email sent successfully to {TO_EMAIL}")
except Exception as e:
    print(f"❌ Failed to send email: {e}")

