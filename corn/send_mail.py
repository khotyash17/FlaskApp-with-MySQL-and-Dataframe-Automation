import smtplib
import os

import pyminizip

from email.message import EmailMessage


print("send_email.py started")
#print(f"[{datetime.datetime.now()}] send_email.py started")

# Gmail credentials (better to store in ENV variables)
EMAIL_ADDRESS = os.getenv("OWNER_EMAIL")
EMAIL_PASSWORD = os.getenv("OWNER_PASS")  # Use Gmail App Password
OWNER_TO = os.getenv("TO_EMAIL")
ZIP_PASS = os.getenv("ZIP_PASS")


EXPORTS_DIR = "/app/exports"


#if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not OWNER_TO or not ZIP_PASS:
#   raise ValueError("❌ Missing environment variables: OWNER_EMAIL / OWNER_PASS / TO_EMAIL / ZIP_PASS")

# Folder where CSVs are stored
# EXPORTS_DIR = "/app/exports"

def get_latest_csv():
    """Find the latest CSV file in exports directory"""
    files = [os.path.join(EXPORTS_DIR, f) for f in os.listdir(EXPORTS_DIR) if f.endswith(".csv")]
    if not files:
        return None
    return max(files, key=os.path.getctime)

#NEW CODE FOR PASS
#def create_password_protected_zip(csv_file):
#    """Create a password-protected ZIP for the given CSV file"""
#    zip_filename = os.path.join(tempfile.gettempdir(), os.path.basename(csv_file).replace(".csv", ".zip"))

#   with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zf:
#        zf.setpassword(ZIP_PASS.encode())
#        zf.write(csv_file, arcname=os.path.basename(csv_file))

#    return zip_filename

def send_email():
    latest_file = get_latest_csv()
    if not latest_file:
        print("No CSV file found to send.")
        return

#CREATEP PASSWORD PROTECTED ZIP
#    zip_file  = create_password_protected_zip(latest_file)

    zip_file = latest_file.replace(".csv", ".zip")
    pyminizip.compress(latest_file, None, zip_file, ZIP_PASS, 5)


    msg = EmailMessage()
    msg["Subject"] = "Daily Students Report"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = OWNER_TO
    msg.set_content(
#        f"Attached is the latest students report."
        f"The file is password protected. \n\nPassword: {ZIP_PASS}"
    )

    with open(zip_file, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="zip", filename=os.path.basename(zip_file))



    # Attach CSV
#    with open(latest_file, "rb") as f:
#       msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=os.path.basename(latest_file))

    # Send email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Sent report {latest_file} to {OWNER_TO}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    send_email()
