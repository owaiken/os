"""
HTTPS Enforcement and Content Security Policy for Owaiken
Implements secure HTTP headers and HTTPS enforcement
"""
import os
import streamlit as st
from typing import Dict, Any, List, Optional, Union
import base64
import hashlib
import secrets

class SecurityHeadersManager:
    """
    Security Headers Manager for Owaiken
    
    Implements HTTP security headers including:
    - Content Security Policy (CSP)
    - Strict Transport Security (HSTS)
    - X-Content-Type-Options
    - X-Frame-Options
    - Referrer-Policy
    - Permissions-Policy
    """
    
    def __init__(self):
        """Initialize the security headers manager"""
        # Generate a random nonce for CSP
        self.nonce = base64.b64encode(secrets.token_bytes(16)).decode('utf-8')
        
        # Default CSP directives
        self.csp_directives = {
            'default-src': ["'self'"],
            'script-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", f"'nonce-{self.nonce}'"],
            'style-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
            'img-src': ["'self'", "data:", "https://cdn.jsdelivr.net"],
            'font-src': ["'self'", "https://cdn.jsdelivr.net"],
            'connect-src': ["'self'", "https://*.supabase.co", "https://*.clerk.dev", "https://*.stripe.com"],
            'frame-src': ["'self'", "https://*.stripe.com", "https://*.clerk.dev"],
            'object-src': ["'none'"],
            'base-uri': ["'self'"],
            'form-action': ["'self'"],
            'frame-ancestors': ["'self'"],
            'upgrade-insecure-requests': []
        }
        
        # Other security headers
        self.security_headers = {
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), interest-cohort=()'
        }
    
    def add_csp_directive(self, directive: str, value: str):
        """
        Add a CSP directive value
        
        Args:
            directive: CSP directive name
            value: Value to add
        """
        if directive in self.csp_directives:
            if value not in self.csp_directives[directive]:
                self.csp_directives[directive].append(value)
        else:
            self.csp_directives[directive] = [value]
    
    def get_csp_header(self) -> str:
        """
        Get the Content-Security-Policy header value
        
        Returns:
            CSP header value
        """
        csp_parts = []
        
        for directive, values in self.csp_directives.items():
            if values:
                csp_parts.append(f"{directive} {' '.join(values)}")
            else:
                csp_parts.append(directive)
        
        return "; ".join(csp_parts)
    
    def get_all_security_headers(self) -> Dict[str, str]:
        """
        Get all security headers
        
        Returns:
            Dictionary of security headers
        """
        headers = self.security_headers.copy()
        headers['Content-Security-Policy'] = self.get_csp_header()
        
        return headers
    
    def apply_security_headers(self):
        """Apply security headers to Streamlit app"""
        # Streamlit doesn't provide direct access to HTTP headers
        # This is a workaround using HTML/JavaScript
        
        headers = self.get_all_security_headers()
        meta_tags = []
        
        # Add CSP as meta tag
        meta_tags.append(f'<meta http-equiv="Content-Security-Policy" content="{headers["Content-Security-Policy"]}">')
        
        # Add other headers as meta tags where possible
        if 'X-Content-Type-Options' in headers:
            meta_tags.append(f'<meta http-equiv="X-Content-Type-Options" content="{headers["X-Content-Type-Options"]}">')
        
        # Inject meta tags into Streamlit
        meta_html = '\n'.join(meta_tags)
        st.markdown(meta_html, unsafe_allow_html=True)
        
        # Return nonce for use in inline scripts
        return self.nonce

def enforce_https():
    """
    Enforce HTTPS for Streamlit app
    
    This is a client-side enforcement since Streamlit doesn't provide
    server-side redirect capabilities
    """
    # JavaScript to redirect HTTP to HTTPS
    redirect_script = """
    <script>
        if (window.location.protocol === 'http:' && 
            window.location.hostname !== 'localhost' && 
            !window.location.hostname.startsWith('127.') && 
            window.location.hostname !== '0.0.0.0') {
            window.location.href = window.location.href.replace('http:', 'https:');
        }
    </script>
    """
    
    st.markdown(redirect_script, unsafe_allow_html=True)

def setup_security_headers():
    """Set up security headers for Streamlit app"""
    # Enforce HTTPS
    enforce_https()
    
    # Initialize security headers manager
    headers_manager = SecurityHeadersManager()
    
    # Add custom CSP directives for Streamlit
    headers_manager.add_csp_directive('script-src', "https://cdn.streamlit.io")
    headers_manager.add_csp_directive('connect-src', "https://cdn.streamlit.io")
    headers_manager.add_csp_directive('connect-src', "wss://cdn.streamlit.io")
    headers_manager.add_csp_directive('img-src', "https://cdn.streamlit.io")
    
    # Apply security headers
    nonce = headers_manager.apply_security_headers()
    
    return nonce
