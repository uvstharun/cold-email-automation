import smtplib
from email.mime.text import MIMEText
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load Google Sheets API Credentials
def get_google_sheet(sheet_url, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json", scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    return sheet

# Email Sending Function
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_SENDER = "uppugundurit@gmail.com"  # Change to your Gmail
EMAIL_PASSWORD = "cgrz eflh wdff hgye"   # Use Google App Password

def send_email(recipient, subject, body):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, msg.as_string())

# Fetch Data from Google Sheets & Send Emails
def send_bulk_emails(sheet_url, sheet_name):
    sheet = get_google_sheet(sheet_url, sheet_name)
    data = sheet.get_all_records()

    for row in data:
        email = row["email"]
        name = row["name"]
        company = row["company"]
        subject = f"Excited to Connect, {name}!"
        body = f"""
        Hi {name},<br><br>
        I came across {company} and I'm really impressed by your work.<br>
        I specialize in {row['your_skill']} and would love to contribute.<br>
        Let’s connect!<br>
        """

        send_email(email, subject, body)
        print(f"Email sent to {email}")