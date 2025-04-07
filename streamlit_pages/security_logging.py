"""
Security Logging and Monitoring Module for Owaiken
Implements comprehensive security event logging and monitoring
"""
import os
import json
import uuid
import time
import logging
import traceback
import socket
import hashlib
import requests
import streamlit as st
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime
from enum import Enum

# Security event types
class SecurityEventType(str, Enum):
    """Security event types for classification and filtering"""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    MFA_ENABLED = "mfa_enabled"
    MFA_DISABLED = "mfa_disabled"
    MFA_CHALLENGE_SUCCESS = "mfa_challenge_success"
    MFA_CHALLENGE_FAILURE = "mfa_challenge_failure"
    RECOVERY_CODE_USED = "recovery_code_used"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_UNLOCKED = "account_unlocked"
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_UPDATED = "subscription_updated"
    SUBSCRIPTION_CANCELLED = "subscription_cancelled"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILURE = "payment_failure"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    API_KEY_CREATED = "api_key_created"
    API_KEY_DELETED = "api_key_deleted"
    PERMISSION_CHANGE = "permission_change"
    DATA_EXPORT = "data_export"
    ADMIN_ACTION = "admin_action"

# Security severity levels
class SecuritySeverity(str, Enum):
    """Security severity levels for prioritization"""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Configure logging
class SecurityLogger:
    """
    Security Logger for Owaiken
    
    Implements comprehensive security event logging with:
    - Structured JSON logging
    - Multiple output destinations
    - Severity-based filtering
    - PII protection
    - Tamper-evident logs
    """
    
    def __init__(
        self,
        app_name: str = "owaiken",
        log_level: int = logging.INFO,
        log_to_file: bool = True,
        log_to_console: bool = True,
        log_to_service: bool = False,
        log_dir: Optional[str] = None,
        log_service_url: Optional[str] = None,
        log_service_key: Optional[str] = None
    ):
        """
        Initialize security logger
        
        Args:
            app_name: Application name
            log_level: Logging level
            log_to_file: Whether to log to file
            log_to_console: Whether to log to console
            log_to_service: Whether to log to external service
            log_dir: Directory for log files
            log_service_url: URL for external logging service
            log_service_key: API key for external logging service
        """
        self.app_name = app_name
        self.host_name = socket.gethostname()
        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        self.log_to_service = log_to_service
        
        # Set up logging
        self.logger = logging.getLogger(f"{app_name}_security")
        self.logger.setLevel(log_level)
        self.logger.propagate = False
        
        # Clear existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Add console handler if enabled
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # Add file handler if enabled
        if log_to_file:
            if not log_dir:
                log_dir = os.path.join(os.getcwd(), "logs")
            
            # Create logs directory if it doesn't exist
            os.makedirs(log_dir, exist_ok=True)
            
            # Create log file with date
            log_file = os.path.join(
                log_dir, 
                f"{app_name}_security_{datetime.now().strftime('%Y%m%d')}.log"
            )
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # Set up external logging service
        if log_to_service:
            self.log_service_url = log_service_url or st.secrets.get(
                "LOG_SERVICE_URL", 
                os.environ.get("LOG_SERVICE_URL")
            )
            self.log_service_key = log_service_key or st.secrets.get(
                "LOG_SERVICE_KEY", 
                os.environ.get("LOG_SERVICE_KEY")
            )
            
            if not self.log_service_url or not self.log_service_key:
                self.log_to_service = False
                self.logger.warning("External logging service not configured properly")
    
    def _mask_pii(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mask personally identifiable information (PII)
        
        Args:
            data: Data dictionary
            
        Returns:
            Data with PII masked
        """
        # Create a copy to avoid modifying the original
        masked_data = data.copy()
        
        # PII fields to mask
        pii_fields = [
            "password", "credit_card", "ssn", "social_security", 
            "address", "phone", "email", "birth", "secret"
        ]
        
        # Mask PII fields
        for key in masked_data:
            lower_key = key.lower()
            
            # Check if key contains any PII field name
            if any(pii in lower_key for pii in pii_fields):
                if isinstance(masked_data[key], str):
                    # Mask with asterisks, keeping first and last characters
                    if len(masked_data[key]) > 4:
                        masked_data[key] = masked_data[key][0] + "*" * (len(masked_data[key]) - 2) + masked_data[key][-1]
                    else:
                        masked_data[key] = "****"
            
            # Recursively mask nested dictionaries
            elif isinstance(masked_data[key], dict):
                masked_data[key] = self._mask_pii(masked_data[key])
            
            # Mask PII in lists of dictionaries
            elif isinstance(masked_data[key], list):
                masked_data[key] = [
                    self._mask_pii(item) if isinstance(item, dict) else item
                    for item in masked_data[key]
                ]
        
        return masked_data
    
    def _calculate_log_hash(self, log_data: Dict[str, Any]) -> str:
        """
        Calculate tamper-evident hash for log entry
        
        Args:
            log_data: Log data dictionary
            
        Returns:
            SHA-256 hash of log data
        """
        # Sort keys for consistent hashing
        serialized = json.dumps(log_data, sort_keys=True)
        
        # Calculate SHA-256 hash
        return hashlib.sha256(serialized.encode()).hexdigest()
    
    def _send_to_external_service(self, log_data: Dict[str, Any]) -> bool:
        """
        Send log to external logging service
        
        Args:
            log_data: Log data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        if not self.log_to_service:
            return False
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.log_service_key}"
            }
            
            response = requests.post(
                self.log_service_url,
                headers=headers,
                json=log_data,
                timeout=5  # 5 second timeout
            )
            
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Failed to send log to external service: {str(e)}")
            return False
    
    def log_security_event(
        self,
        event_type: SecurityEventType,
        user_id: Optional[str] = None,
        severity: SecuritySeverity = SecuritySeverity.INFO,
        details: Optional[Dict[str, Any]] = None,
        source_ip: Optional[str] = None,
        mask_pii: bool = True
    ) -> str:
        """
        Log a security event
        
        Args:
            event_type: Type of security event
            user_id: User ID (optional)
            severity: Severity level
            details: Additional details
            source_ip: Source IP address
            mask_pii: Whether to mask PII
            
        Returns:
            Log entry ID
        """
        # Generate log entry ID
        log_id = str(uuid.uuid4())
        
        # Create log data
        log_data = {
            "id": log_id,
            "timestamp": datetime.now().isoformat(),
            "app": self.app_name,
            "host": self.host_name,
            "event_type": event_type,
            "severity": severity,
            "user_id": user_id,
            "source_ip": source_ip,
            "details": details or {}
        }
        
        # Mask PII if enabled
        if mask_pii:
            log_data = self._mask_pii(log_data)
        
        # Add tamper-evident hash
        log_data["hash"] = self._calculate_log_hash(log_data)
        
        # Convert to JSON
        log_json = json.dumps(log_data)
        
        # Log based on severity
        if severity == SecuritySeverity.CRITICAL:
            self.logger.critical(log_json)
        elif severity == SecuritySeverity.HIGH:
            self.logger.error(log_json)
        elif severity == SecuritySeverity.MEDIUM:
            self.logger.warning(log_json)
        elif severity == SecuritySeverity.LOW:
            self.logger.info(log_json)
        else:
            self.logger.debug(log_json)
        
        # Send to external service if enabled
        if self.log_to_service:
            self._send_to_external_service(log_data)
        
        return log_id
    
    def log_login_attempt(
        self,
        user_id: str,
        success: bool,
        source_ip: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log a login attempt
        
        Args:
            user_id: User ID
            success: Whether login was successful
            source_ip: Source IP address
            details: Additional details
            
        Returns:
            Log entry ID
        """
        event_type = SecurityEventType.LOGIN_SUCCESS if success else SecurityEventType.LOGIN_FAILURE
        severity = SecuritySeverity.INFO if success else SecuritySeverity.MEDIUM
        
        return self.log_security_event(
            event_type=event_type,
            user_id=user_id,
            severity=severity,
            details=details,
            source_ip=source_ip
        )
    
    def log_mfa_attempt(
        self,
        user_id: str,
        success: bool,
        method: str = "totp",
        source_ip: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log an MFA attempt
        
        Args:
            user_id: User ID
            success: Whether MFA was successful
            method: MFA method (totp, recovery, etc.)
            source_ip: Source IP address
            details: Additional details
            
        Returns:
            Log entry ID
        """
        event_type = SecurityEventType.MFA_CHALLENGE_SUCCESS if success else SecurityEventType.MFA_CHALLENGE_FAILURE
        severity = SecuritySeverity.INFO if success else SecuritySeverity.MEDIUM
        
        details = details or {}
        details["mfa_method"] = method
        
        return self.log_security_event(
            event_type=event_type,
            user_id=user_id,
            severity=severity,
            details=details,
            source_ip=source_ip
        )
    
    def log_subscription_event(
        self,
        user_id: str,
        event_type: SecurityEventType,
        subscription_id: str,
        plan: str,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log a subscription event
        
        Args:
            user_id: User ID
            event_type: Subscription event type
            subscription_id: Subscription ID
            plan: Subscription plan
            details: Additional details
            
        Returns:
            Log entry ID
        """
        details = details or {}
        details["subscription_id"] = subscription_id
        details["plan"] = plan
        
        return self.log_security_event(
            event_type=event_type,
            user_id=user_id,
            severity=SecuritySeverity.INFO,
            details=details
        )
    
    def log_rate_limit_exceeded(
        self,
        user_id: Optional[str],
        endpoint: str,
        limit: int,
        window: str,
        source_ip: Optional[str] = None
    ) -> str:
        """
        Log a rate limit exceeded event
        
        Args:
            user_id: User ID (optional)
            endpoint: API endpoint
            limit: Rate limit
            window: Rate limit window
            source_ip: Source IP address
            
        Returns:
            Log entry ID
        """
        details = {
            "endpoint": endpoint,
            "limit": limit,
            "window": window
        }
        
        return self.log_security_event(
            event_type=SecurityEventType.RATE_LIMIT_EXCEEDED,
            user_id=user_id,
            severity=SecuritySeverity.MEDIUM,
            details=details,
            source_ip=source_ip
        )
    
    def log_suspicious_activity(
        self,
        user_id: Optional[str],
        activity_type: str,
        severity: SecuritySeverity = SecuritySeverity.HIGH,
        source_ip: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log suspicious activity
        
        Args:
            user_id: User ID (optional)
            activity_type: Type of suspicious activity
            severity: Severity level
            source_ip: Source IP address
            details: Additional details
            
        Returns:
            Log entry ID
        """
        details = details or {}
        details["activity_type"] = activity_type
        
        return self.log_security_event(
            event_type=SecurityEventType.SUSPICIOUS_ACTIVITY,
            user_id=user_id,
            severity=severity,
            details=details,
            source_ip=source_ip
        )

# Get security logger instance
def get_security_logger():
    """Get or create the security logger instance"""
    if "security_logger" not in st.session_state:
        # Get configuration from environment or secrets
        log_to_file = st.secrets.get("SECURITY_LOG_TO_FILE", os.environ.get("SECURITY_LOG_TO_FILE", "true")).lower() == "true"
        log_to_console = st.secrets.get("SECURITY_LOG_TO_CONSOLE", os.environ.get("SECURITY_LOG_TO_CONSOLE", "true")).lower() == "true"
        log_to_service = st.secrets.get("SECURITY_LOG_TO_SERVICE", os.environ.get("SECURITY_LOG_TO_SERVICE", "false")).lower() == "true"
        
        # Create logger
        st.session_state.security_logger = SecurityLogger(
            log_to_file=log_to_file,
            log_to_console=log_to_console,
            log_to_service=log_to_service
        )
    
    return st.session_state.security_logger
