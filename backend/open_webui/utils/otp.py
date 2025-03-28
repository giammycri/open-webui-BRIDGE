import secrets
import time
from typing import Dict, Tuple

# Store OTPs in memory with expiration times (in a production environment, consider using Redis)
otp_store: Dict[str, Tuple[str, int]] = {}  # email -> (otp, expiration_timestamp)
OTP_EXPIRATION_SECONDS = 600  # 10 minutes

def generate_otp(email: str) -> str:
    """Generate a 6-digit OTP for the given email and store it"""
    otp = ''.join(secrets.choice('0123456789') for _ in range(6))
    expiration = int(time.time()) + OTP_EXPIRATION_SECONDS
    otp_store[email] = (otp, expiration)
    return otp

def verify_otp(email: str, otp: str) -> bool:
    """Verify if the provided OTP is valid for the email"""
    if email not in otp_store:
        return False
    
    stored_otp, expiration = otp_store[email]
    if time.time() > expiration:
        # OTP expired
        del otp_store[email]
        return False
    
    if otp == stored_otp:
        # OTP verified, clean up
        del otp_store[email]
        return True
    
    return False

def get_otp_for_email(email: str) -> str:
    """Get the OTP for an email (for development/testing purposes)"""
    if email in otp_store:
        return otp_store[email][0]
    return ""