import random  # Aggiungi questa riga
import secrets
import time
from typing import Dict, Tuple

# Store OTPs in memory with expiration times (in a production environment, consider using Redis)
otp_store: Dict[str, Tuple[str, int]] = {}  # email -> (otp, expiration_timestamp)
OTP_EXPIRATION_SECONDS = 600  # 10 minutes

def generate_otp(email: str) -> str:
    """Generate a 6-digit OTP code and store it with email as key"""
    # Generate a 6-digit OTP
    otp = ''.join(random.choices('0123456789', k=6))
    
    # Store the OTP in memory (versione semplificata invece di redis)
    expiration_time = int(time.time()) + OTP_EXPIRATION_SECONDS
    otp_store[email] = (otp, expiration_time)
    
    return otp

def verify_otp(email: str, otp: str) -> bool:
    """Verify if the provided OTP matches the one stored for the email"""
    if email not in otp_store:
        return False
    
    stored_otp, expiration_time = otp_store[email]
    current_time = int(time.time())
    
    if current_time > expiration_time:
        # OTP expired
        del otp_store[email]
        return False
    
    if stored_otp == otp:
        # OTP valid, remove it after successful verification
        del otp_store[email]
        return True
    
    return False

def get_otp_for_email(email: str) -> str:
    """Get the OTP for an email (for development/testing purposes)"""
    if email in otp_store:
        return otp_store[email][0]
    return ""