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
    # Hard-coded values from environment variables we know exist
    supabase_url = "https://effhhuuhualzawjtnczv.supabase.co"
    print(f"Using hardcoded Supabase URL: {supabase_url}")
    
    # Print all environment variables for debugging (redacting sensitive values)
    print("\n=== ENVIRONMENT VARIABLES ===\n")
    for key, value in os.environ.items():
        if any(sensitive in key.lower() for sensitive in ["key", "secret", "password", "token"]):
            print(f"{key}: [REDACTED]")
        else:
            print(f"{key}: {value}")
    print("\n=== END ENVIRONMENT VARIABLES ===\n")
    
    # Get the service key directly
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    print(f"SUPABASE_SERVICE_KEY found: {supabase_key is not None}")
    
    if not supabase_key:
        # Fallback to other key names
        for key_name in ["SUPABASE_KEY", "SUPABASE_ANON_KEY"]:
            if key_name in os.environ:
                supabase_key = os.environ.get(key_name)
                print(f"Using {key_name} for Supabase connection")
                break
    else:
        print("Using SUPABASE_SERVICE_KEY for connection")
    
    if not supabase_url or not supabase_key:
        print("Missing Supabase credentials in environment variables")
        return None
    
    try:
        # Create client directly
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None
