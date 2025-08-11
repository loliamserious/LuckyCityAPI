import os
from dotenv import load_dotenv
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# Email configuration
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_SERVER = os.getenv("MAIL_SERVER")

async def send_email(to_email: str, subject: str, body: str):
    """Send email using aiosmtplib."""
    message = MIMEMultipart()
    message["From"] = MAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "html"))

    await aiosmtplib.send(
        message,
        hostname=MAIL_SERVER,
        port=MAIL_PORT,
        username=MAIL_USERNAME,
        password=MAIL_PASSWORD,
        use_tls=True
    ) 