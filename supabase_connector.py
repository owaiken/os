"""
Direct Supabase Connector for Owaiken

This module provides a secure connection to Supabase that works with both
admin deployments and end-user configurations.
"""

import os
import streamlit as st
from supabase import create_client, Client

def get_direct_supabase_client() -> Client:
    """
    Get a Supabase client by securely accessing credentials
    
    This function prioritizes user-specific credentials over deployment credentials,
    ensuring that users with licenses can connect to their own Supabase instances.
    
    Returns:
        Client: Supabase client or None if connection fails
    """
    # First check for user-specific credentials in Streamlit session state
    # This ensures users with licenses can use their own Supabase
    if hasattr(st, 'session_state') and 'user_supabase_url' in st.session_state and 'user_supabase_key' in st.session_state:
        supabase_url = st.session_state.user_supabase_url
        supabase_key = st.session_state.user_supabase_key
        print("Using user-specific Supabase credentials from session state")
    else:
        # Fall back to environment variables
        supabase_url = os.environ.get("SUPABASE_URL")
        
        # Try multiple key names for compatibility
        supabase_key = None
        for key_name in ["SUPABASE_SERVICE_KEY", "SUPABASE_KEY", "SUPABASE_ANON_KEY"]:
            if key_name in os.environ:
                supabase_key = os.environ.get(key_name)
                print(f"Using {key_name} from environment variables")
                break
    
    if not supabase_url or not supabase_key:
        print("Missing Supabase credentials in environment variables")
        return None
    
    try:
        # Create client directly
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None
