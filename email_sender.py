import smtplib
from email.mime.text import MIMEText
import subprocess
import sys

try:
    import gspread
except ModuleNotFoundError:
    subprocess.run([sys.executable, "-m", "pip", "install", "gspread"])
    import gspread  # Retry import
from oauth2client.service_account import ServiceAccountCredentials
import json
import streamlit as st

# ✅ Load Google API Credentials from Streamlit Secrets
google_creds = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])

# ✅ Authenticate with Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
client = gspread.authorize(creds)

# ✅ Fetch data from Google Sheets
def get_google_sheet(sheet_url, sheet_name):
    try:
        sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
        return sheet
    except Exception as e:
        st.error(f"Failed to fetch Google Sheet: {e}")
        return None

# ✅ Load Email Credentials from Streamlit Secrets
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_SENDER = st.secrets["EMAIL_SENDER"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

# ✅ Email sending function with error handling
def send_email(recipient, subject, body):
    try:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        return True  # Email sent successfully
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")
        return False  # Email sending failed

# ✅ Send bulk emails from Google Sheets & mark sent emails
def send_bulk_emails(sheet_url, sheet_name):
    sheet = get_google_sheet(sheet_url, sheet_name)
    if not sheet:
        return

    data = sheet.get_all_records()

    for i, row in enumerate(data, start=2):  # Start from row 2 (assuming row 1 is headers)
        email = row.get("email")
        name = row.get("name")
        company = row.get("company", "your company")  # Default fallback
        sent_status = row.get("sent_status", "")  # Check if email was already sent

        if email and name and sent_status.lower() != "sent":  # Avoid re-sending emails
            subject = f"Excited to Connect, {name}!"
            body = f"""
            Hi {name},<br><br>
            I came across {company} and I’m really impressed.<br>
            Let’s connect!
            """

            if send_email(email, subject, body):
                sheet.update_cell(i, 4, "Sent")  # ✅ Mark email as "Sent" in Google Sheets
                print(f"✅ Email sent to {email}")
            else:
                print(f"❌ Failed to send email to {email}")