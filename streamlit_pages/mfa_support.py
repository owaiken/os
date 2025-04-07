"""
Multi-Factor Authentication (MFA) Module for Owaiken
Implements industry-standard MFA using TOTP and recovery codes
"""
import os
import time
import base64
import hmac
import hashlib
import secrets
import qrcode
import pyotp
from io import BytesIO
import streamlit as st
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta

class MFAManager:
    """
    Multi-Factor Authentication Manager for Owaiken
    - Implements TOTP (Time-based One-Time Password) according to RFC 6238
    - Generates and validates backup/recovery codes
    - Provides secure enrollment and verification flows
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize MFA Manager
        
        Args:
            secret_key: Secret key for HMAC operations (optional)
        """
        # Use provided key or get from environment/secrets
        self.secret_key = secret_key or st.secrets.get(
            "MFA_SECRET_KEY", 
            os.environ.get("MFA_SECRET_KEY", secrets.token_hex(32))
        )
    
    def generate_totp_secret(self) -> str:
        """
        Generate a new TOTP secret for a user
        
        Returns:
            Base32 encoded secret compatible with authenticator apps
        """
        # Generate a cryptographically secure random secret
        # 160 bits (20 bytes) as recommended by RFC 4226
        random_bytes = secrets.token_bytes(20)
        
        # Encode in Base32 as required by TOTP standard
        secret = base64.b32encode(random_bytes).decode('utf-8')
        
        return secret
    
    def get_totp_uri(self, secret: str, user_email: str, issuer: str = "Owaiken") -> str:
        """
        Get otpauth URI for QR code generation
        
        Args:
            secret: TOTP secret
            user_email: User's email
            issuer: Name of the issuer (app name)
            
        Returns:
            otpauth URI for QR code
        """
        return f"otpauth://totp/{issuer}:{user_email}?secret={secret}&issuer={issuer}"
    
    def generate_qr_code(self, uri: str) -> str:
        """
        Generate QR code for TOTP URI
        
        Args:
            uri: TOTP URI
            
        Returns:
            Base64 encoded QR code image
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
    
    def verify_totp(self, secret: str, code: str) -> bool:
        """
        Verify a TOTP code
        
        Args:
            secret: TOTP secret
            code: TOTP code to verify
            
        Returns:
            True if code is valid, False otherwise
        """
        totp = pyotp.TOTP(secret)
        
        # Verify with a window of ±1 time step to account for clock skew
        return totp.verify(code, valid_window=1)
    
    def generate_recovery_codes(self, count: int = 10) -> List[str]:
        """
        Generate recovery codes for backup access
        
        Args:
            count: Number of recovery codes to generate
            
        Returns:
            List of recovery codes
        """
        codes = []
        for _ in range(count):
            # Generate a 10-character code with 4 groups of 5 characters
            code = secrets.token_hex(10)
            formatted_code = '-'.join([code[i:i+5] for i in range(0, 20, 5)])
            codes.append(formatted_code)
        
        return codes
    
    def hash_recovery_codes(self, codes: List[str]) -> List[str]:
        """
        Hash recovery codes for secure storage
        
        Args:
            codes: List of recovery codes
            
        Returns:
            List of hashed recovery codes
        """
        hashed_codes = []
        for code in codes:
            # Remove formatting
            clean_code = code.replace('-', '')
            
            # Create HMAC using secret key
            h = hmac.new(
                self.secret_key.encode(),
                clean_code.encode(),
                hashlib.sha256
            )
            hashed_codes.append(h.hexdigest())
        
        return hashed_codes
    
    def verify_recovery_code(self, code: str, hashed_codes: List[str]) -> bool:
        """
        Verify a recovery code against hashed codes
        
        Args:
            code: Recovery code to verify
            hashed_codes: List of hashed recovery codes
            
        Returns:
            True if code is valid, False otherwise
        """
        # Remove formatting
        clean_code = code.replace('-', '')
        
        # Create HMAC using secret key
        h = hmac.new(
            self.secret_key.encode(),
            clean_code.encode(),
            hashlib.sha256
        )
        code_hash = h.hexdigest()
        
        # Check if hash is in the list of hashed codes
        return code_hash in hashed_codes

# MFA Enrollment Flow
def display_mfa_enrollment(user_id: str, user_email: str) -> Dict[str, Any]:
    """
    Display MFA enrollment flow
    
    Args:
        user_id: User ID
        user_email: User email
        
    Returns:
        Dict with enrollment status and data
    """
    # Initialize MFA manager
    mfa_manager = MFAManager()
    
    # Initialize session state for MFA enrollment
    if "mfa_enrollment_step" not in st.session_state:
        st.session_state.mfa_enrollment_step = 1
        st.session_state.mfa_secret = mfa_manager.generate_totp_secret()
        st.session_state.mfa_recovery_codes = mfa_manager.generate_recovery_codes()
        st.session_state.mfa_hashed_recovery_codes = mfa_manager.hash_recovery_codes(
            st.session_state.mfa_recovery_codes
        )
    
    # Step 1: Display QR code
    if st.session_state.mfa_enrollment_step == 1:
        st.subheader("Set Up Two-Factor Authentication")
        st.write("Scan this QR code with your authenticator app (Google Authenticator, Authy, etc.)")
        
        # Generate QR code
        uri = mfa_manager.get_totp_uri(st.session_state.mfa_secret, user_email)
        qr_code = mfa_manager.generate_qr_code(uri)
        
        # Display QR code
        st.image(f"data:image/png;base64,{qr_code}", width=300)
        
        # Manual entry option
        with st.expander("Can't scan the QR code?"):
            st.code(st.session_state.mfa_secret)
            st.write("Enter this code manually in your authenticator app")
        
        # Verification form
        with st.form("verify_mfa"):
            verification_code = st.text_input("Enter the 6-digit code from your authenticator app")
            verify_button = st.form_submit_button("Verify")
            
            if verify_button:
                if mfa_manager.verify_totp(st.session_state.mfa_secret, verification_code):
                    st.success("Verification successful!")
                    st.session_state.mfa_enrollment_step = 2
                    st.rerun()
                else:
                    st.error("Invalid code. Please try again.")
    
    # Step 2: Display recovery codes
    elif st.session_state.mfa_enrollment_step == 2:
        st.subheader("Recovery Codes")
        st.write("Save these recovery codes in a secure place. You can use them to access your account if you lose your authenticator device.")
        st.warning("These codes will only be shown once!")
        
        # Display recovery codes
        for code in st.session_state.mfa_recovery_codes:
            st.code(code)
        
        # Download option
        recovery_codes_text = "\n".join(st.session_state.mfa_recovery_codes)
        st.download_button(
            "Download Recovery Codes",
            recovery_codes_text,
            "owaiken_recovery_codes.txt",
            "text/plain"
        )
        
        # Confirmation
        if st.button("I've saved my recovery codes"):
            st.session_state.mfa_enrollment_step = 3
            st.rerun()
    
    # Step 3: Completion
    elif st.session_state.mfa_enrollment_step == 3:
        st.success("Two-factor authentication has been enabled for your account!")
        st.write("You'll now need to enter a verification code when you sign in.")
        
        # Return enrollment data
        enrollment_data = {
            "user_id": user_id,
            "secret": st.session_state.mfa_secret,
            "hashed_recovery_codes": st.session_state.mfa_hashed_recovery_codes,
            "enabled": True,
            "enrolled_at": datetime.now().isoformat()
        }
        
        # Clear session state
        st.session_state.pop("mfa_enrollment_step", None)
        st.session_state.pop("mfa_recovery_codes", None)
        
        return enrollment_data
    
    # Return None if enrollment is not complete
    return None

# MFA Verification Flow
def display_mfa_verification(user_id: str, mfa_data: Dict[str, Any]) -> bool:
    """
    Display MFA verification flow
    
    Args:
        user_id: User ID
        mfa_data: MFA data for the user
        
    Returns:
        True if verification is successful, False otherwise
    """
    # Initialize MFA manager
    mfa_manager = MFAManager()
    
    # Initialize session state for MFA verification
    if "mfa_verification_step" not in st.session_state:
        st.session_state.mfa_verification_step = 1
    
    # Step 1: TOTP verification
    if st.session_state.mfa_verification_step == 1:
        st.subheader("Two-Factor Authentication")
        st.write("Enter the 6-digit code from your authenticator app")
        
        # Verification form
        with st.form("verify_mfa"):
            verification_code = st.text_input("Authentication Code")
            verify_button = st.form_submit_button("Verify")
            
            if verify_button:
                if mfa_manager.verify_totp(mfa_data["secret"], verification_code):
                    st.success("Verification successful!")
                    
                    # Clear session state
                    st.session_state.pop("mfa_verification_step", None)
                    
                    return True
                else:
                    st.error("Invalid code. Please try again.")
        
        # Recovery option
        if st.button("Use a recovery code"):
            st.session_state.mfa_verification_step = 2
            st.rerun()
    
    # Step 2: Recovery code verification
    elif st.session_state.mfa_verification_step == 2:
        st.subheader("Recovery Code Verification")
        st.write("Enter one of your recovery codes")
        
        # Recovery form
        with st.form("recovery_code"):
            recovery_code = st.text_input("Recovery Code")
            verify_button = st.form_submit_button("Verify")
            
            if verify_button:
                if mfa_manager.verify_recovery_code(
                    recovery_code, 
                    mfa_data["hashed_recovery_codes"]
                ):
                    st.success("Recovery code accepted!")
                    
                    # Remove used recovery code
                    # In a real implementation, you would update the stored hashed_recovery_codes
                    
                    # Clear session state
                    st.session_state.pop("mfa_verification_step", None)
                    
                    return True
                else:
                    st.error("Invalid recovery code. Please try again.")
        
        # Back to TOTP
        if st.button("Back to authenticator verification"):
            st.session_state.mfa_verification_step = 1
            st.rerun()
    
    # Return False if verification is not complete
    return False

# Get MFA manager instance
def get_mfa_manager():
    """Get or create the MFA manager instance"""
    if "mfa_manager" not in st.session_state:
        st.session_state.mfa_manager = MFAManager()
    
    return st.session_state.mfa_manager
