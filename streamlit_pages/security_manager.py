"""
Comprehensive Security Manager for Owaiken
Integrates all security components into a unified system
"""
import os
import streamlit as st
from typing import Dict, Any, List, Optional, Union, Callable

# Import all security modules
from streamlit_pages.rate_limiting import get_rate_limiter, OwaikanRateLimiter
from streamlit_pages.mfa_support import get_mfa_manager, MFAManager
from streamlit_pages.prepared_statements import get_prepared_statement_manager, PreparedStatementManager
from streamlit_pages.security_logging import get_security_logger, SecurityLogger, SecurityEventType, SecuritySeverity
from streamlit_pages.https_enforcement import setup_security_headers
from streamlit_pages.security_config import initialize_database_security

class SecurityManager:
    """
    Comprehensive Security Manager for Owaiken
    
    Integrates all security components:
    - Rate limiting
    - Multi-factor authentication
    - Prepared statements
    - Security logging
    - HTTPS enforcement
    - Row-level security
    """
    
    def __init__(self):
        """Initialize the security manager"""
        # Initialize all security components
        self.rate_limiter = get_rate_limiter()
        self.mfa_manager = get_mfa_manager()
        self.prepared_statements = get_prepared_statement_manager()
        self.security_logger = get_security_logger()
        
        # Set up security headers
        self.csp_nonce = setup_security_headers()
        
        # Initialize database security
        initialize_database_security()
        
        # Log initialization
        self.security_logger.log_security_event(
            event_type=SecurityEventType.ADMIN_ACTION,
            severity=SecuritySeverity.INFO,
            details={"action": "security_manager_initialized"}
        )
    
    def rate_limit(
        self,
        user_id: str,
        tier: str = "free",
        endpoint: str = "default"
    ) -> Dict[str, bool]:
        """
        Check rate limits for a user
        
        Args:
            user_id: User ID
            tier: Subscription tier
            endpoint: API endpoint or feature name
            
        Returns:
            Dict with rate limit status
        """
        result = self.rate_limiter.check_rate_limit(user_id, tier)
        
        # Log rate limit exceeded events
        if result["is_limited"]:
            window = "minute" if result["minute_limited"] else "hour" if result["hour_limited"] else "day"
            self.security_logger.log_rate_limit_exceeded(
                user_id=user_id,
                endpoint=endpoint,
                limit=self.rate_limiter.tier_limits[tier][window],
                window=window
            )
        
        return result
    
    def secure_function(
        self,
        rate_limit_tier: str = "free",
        require_mfa: bool = False,
        log_access: bool = True,
        endpoint_name: Optional[str] = None
    ):
        """
        Decorator for securing functions with multiple security features
        
        Args:
            rate_limit_tier: Rate limit tier to apply
            require_mfa: Whether to require MFA
            log_access: Whether to log access
            endpoint_name: Name of endpoint for logging
            
        Returns:
            Decorator function
        """
        def decorator(func):
            # Get function name if endpoint_name not provided
            nonlocal endpoint_name
            if not endpoint_name:
                endpoint_name = func.__name__
            
            def wrapper(*args, **kwargs):
                # Get user ID from session
                user_id = st.session_state.get("user_id", "anonymous")
                
                # Check rate limits
                rate_limit_result = self.rate_limit(user_id, rate_limit_tier, endpoint_name)
                if rate_limit_result["is_limited"]:
                    st.error("Rate limit exceeded. Please try again later.")
                    return None
                
                # Check MFA if required
                if require_mfa and user_id != "anonymous":
                    # In a real implementation, check if user has completed MFA challenge
                    mfa_verified = st.session_state.get("mfa_verified", False)
                    if not mfa_verified:
                        st.error("Multi-factor authentication required.")
                        return None
                
                # Log access
                if log_access:
                    self.security_logger.log_security_event(
                        event_type=SecurityEventType.API_KEY_CREATED,  # Using as generic access event
                        user_id=user_id,
                        severity=SecuritySeverity.INFO,
                        details={"endpoint": endpoint_name}
                    )
                
                # Execute the function
                return func(*args, **kwargs)
            
            return wrapper
        
        return decorator
    
    def log_login(self, user_id: str, success: bool, source_ip: Optional[str] = None):
        """Log login attempt"""
        self.security_logger.log_login_attempt(user_id, success, source_ip)
    
    def log_mfa(self, user_id: str, success: bool, method: str = "totp"):
        """Log MFA attempt"""
        self.security_logger.log_mfa_attempt(user_id, success, method)
    
    def log_subscription(
        self,
        user_id: str,
        event_type: SecurityEventType,
        subscription_id: str,
        plan: str
    ):
        """Log subscription event"""
        self.security_logger.log_subscription_event(
            user_id, event_type, subscription_id, plan
        )
    
    def detect_suspicious_activity(
        self,
        user_id: str,
        activity_data: Dict[str, Any]
    ) -> bool:
        """
        Detect suspicious activity
        
        Args:
            user_id: User ID
            activity_data: Activity data for analysis
            
        Returns:
            True if activity is suspicious, False otherwise
        """
        # Implement suspicious activity detection logic
        # This is a placeholder for a more sophisticated implementation
        suspicious = False
        
        # Example: Check for rapid succession of actions
        if activity_data.get("action_count", 0) > 20 and activity_data.get("time_window", 60) < 10:
            suspicious = True
            self.security_logger.log_suspicious_activity(
                user_id=user_id,
                activity_type="rapid_actions",
                details=activity_data
            )
        
        # Example: Check for unusual access patterns
        if activity_data.get("unusual_location", False):
            suspicious = True
            self.security_logger.log_suspicious_activity(
                user_id=user_id,
                activity_type="unusual_location",
                details=activity_data
            )
        
        return suspicious

# Get security manager instance
def get_security_manager():
    """Get or create the security manager instance"""
    if "security_manager" not in st.session_state:
        st.session_state.security_manager = SecurityManager()
    
    return st.session_state.security_manager

# Initialize security
def initialize_security():
    """Initialize all security components"""
    security_manager = get_security_manager()
    return security_manager
