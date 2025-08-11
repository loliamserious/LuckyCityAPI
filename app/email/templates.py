from typing import Dict

def get_password_reset_email(email_to: str, token: str, frontend_url: str) -> Dict[str, str]:

    reset_url = f"{frontend_url}/reset-password?token={token}"
    
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

    return {
        "subject": "Password Reset Request",
        "body": html_body
    } 