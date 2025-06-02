import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def send_email(subject, body):
    # Check credentials
    if not (EMAIL_USER and EMAIL_PASSWORD and EMAIL_RECEIVER):
        print("[EMAIL ERROR] Missing email credentials in .env file.")
        return

    try:
        # Construct email
        msg = MIMEText(body, "plain")
        msg["From"] = formataddr(("SPY Options Bot", EMAIL_USER))
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            try:
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
                print("[EMAIL] ✅ Daily report sent.")
            except smtplib.SMTPAuthenticationError as ae:
                print(f"[EMAIL ERROR] Authentication failed: {ae}")
            except Exception as e:
                print(f"[EMAIL ERROR] Failed to send message: {e}")

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to build/send email: {e}")
