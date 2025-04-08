"""
Direct Supabase Connector for Owaiken

This module provides a direct connection to Supabase that bypasses the problematic
credential loading in the original code.
"""

import os
from supabase import create_client, Client

def get_direct_supabase_client() -> Client:
    """
    Get a Supabase client by directly accessing environment variables
    
    Returns:
        Client: Supabase client or None if connection fails
    """
    # Directly access environment variables
    supabase_url = os.environ.get("SUPABASE_URL")
    
    # Try multiple key names
    supabase_key = None
    for key_name in ["SUPABASE_SERVICE_KEY", "SUPABASE_KEY", "SUPABASE_ANON_KEY"]:
        if key_name in os.environ:
            supabase_key = os.environ.get(key_name)
            print(f"Using {key_name} for Supabase connection")
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
