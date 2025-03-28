import logging
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

log = logging.getLogger(__name__)

# Gmail credentials
GMAIL_USERNAME = "bridgeseaeu@gmail.com"
GMAIL_PASSWORD = "hsrj ctjw qjor kjuc"

def send_email(recipient: str, subject: str, body_html: str, body_text: str = None) -> bool:
    """Send an email to the recipient using direct SMTP implementation"""
    try:
        log.info(f"Attempting to send email to {recipient}")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = GMAIL_USERNAME
        msg['To'] = recipient
        
        if body_text:
            part1 = MIMEText(body_text, 'plain')
            msg.attach(part1)
            
        part2 = MIMEText(body_html, 'html')
        msg.attach(part2)
        
        # Direct implementation based on the working test script
        log.info("Creating SMTP connection to smtp.gmail.com:587")
        smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        smtp.set_debuglevel(2)  # Increase debug level
        
        log.info("Sending EHLO")
        smtp.ehlo()
        
        log.info("Starting TLS")
        smtp.starttls()
        
        log.info("Re-sending EHLO after TLS")
        smtp.ehlo()
        
        log.info("Attempting login")
        smtp.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        
        log.info("Sending email")
        smtp.sendmail(GMAIL_USERNAME, recipient, msg.as_string())
        
        log.info("Quitting SMTP session")
        smtp.quit()
        
        log.info("Email sent successfully!")
        return True
        
    except Exception as e:
        log.error(f"Failed to send email: {str(e)}")
        import traceback
        log.error(f"Traceback: {traceback.format_exc()}")
        return False

def send_otp_email(email: str, otp: str, webui_name: str = "BRIDGE") -> bool:
    """Send OTP verification email with customized BRIDGE branding"""
    subject = f"BRIDGE - Verify Your Email"
    
    # Format OTP with spaces for better readability
    formatted_otp = " ".join(otp)
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                color: #333333;
                background-color: #f9f9f9;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                background-color: #1E88E5;
                color: white;
                padding: 30px 20px;
                text-align: center;
            }}
            .content {{
                padding: 30px 20px;
                text-align: center;
            }}
            .otp-code {{
                font-size: 32px;
                font-weight: bold;
                letter-spacing: 5px;
                padding: 20px;
                margin: 20px 0;
                background-color: #f0f7ff;
                border-radius: 8px;
                border: 1px dashed #1E88E5;
                color: #1E88E5;
            }}
            .message {{
                margin-bottom: 30px;
                font-size: 16px;
                line-height: 1.6;
            }}
            .footer {{
                padding: 20px;
                background-color: #f5f5f5;
                text-align: center;
                font-size: 12px;
                color: #666666;
            }}
            h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .logo {{
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 25px;
                background-color: #1E88E5;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-weight: bold;
                margin-top: 20px;
            }}
            .expiry-note {{
                font-size: 14px;
                color: #666666;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">BRIDGE</div>
                <h1>Email Verification</h1>
            </div>
            <div class="content">
                <div class="message">
                    <p>Hello,</p>
                    <p>Thank you for registering with BRIDGE. To complete your account setup, please verify your email address using the verification code below:</p>
                </div>
                <div class="otp-code">{otp}</div>
                <p class="expiry-note">This code will expire in 10 minutes.</p>
                <p>If you didn't request this code, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>&copy; {2025} BRIDGE. All rights reserved.</p>
                <p>This is an automated message, please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    BRIDGE - Email Verification

    Hello,
    
    Thank you for registering with BRIDGE. To complete your account setup, please verify your email address using the verification code below:
    
    {otp}
    
    This code will expire in 10 minutes.
    
    If you didn't request this code, please ignore this email.
    
    © 2025 BRIDGE. All rights reserved.
    This is an automated message, please do not reply to this email.
    """
    
    return send_email(email, subject, html_content, text_content)