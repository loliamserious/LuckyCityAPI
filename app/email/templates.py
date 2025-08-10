from fastapi_mail import MessageSchema
from typing import List
from pydantic import EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

# Get the frontend URL from environment variable, default to localhost for development
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

def get_password_reset_email(email_to: str, token: str) -> MessageSchema:
    # Create the reset password URL
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"
    
    # HTML version for better looking email
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>Password Reset Request</h2>
            <p>Hello,</p>
            <p>You have requested to reset your password. Click the link below to set a new password:</p>
            <p>
                <a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 12px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">
                    Reset Password
                </a>
            </p>
            <p>This link will expire in 15 minutes.</p>
            <p>If you did not request this reset, please ignore this email.</p>
            <br>
            <p>Best regards,<br>Your App Team</p>
            <hr>
            <p style="font-size: 12px; color: #666;">
                If the button doesn't work, copy and paste this link into your browser:<br>
                {reset_url}
            </p>
        </body>
    </html>
    """

    return MessageSchema(
        subject="Password Reset Request",
        recipients=[email_to],
        body=html_body,
        subtype="html"
    ) 