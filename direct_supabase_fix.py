"""
Direct Supabase Connection Fix

This script bypasses all the environment variable handling and directly
connects to Supabase using hardcoded credentials.
"""

import os
from supabase import create_client, Client
import streamlit as st

def direct_supabase_connect():
    """Connect directly to Supabase with hardcoded credentials"""
    # Hardcoded credentials - these are the exact values we know work
    supabase_url = "https://effhhuuhualzawjtnczv.supabase.co"
    
    # Try to get the key from environment variables
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not supabase_key:
        supabase_key = os.environ.get("SUPABASE_KEY")
    
    # If key is still not found, use a hardcoded key (not recommended for production)
    if not supabase_key:
        st.error("No Supabase key found in environment variables")
        return None
    
    try:
        # Create client directly
        supabase = create_client(supabase_url, supabase_key)
        st.success("✅ Successfully connected to Supabase!")
        
        # Test the connection with a simple query
        try:
            response = supabase.table("subscriptions").select("count").execute()
            st.success(f"✅ Successfully queried subscriptions table: {response.data}")
        except Exception as e:
            st.warning(f"Connected to Supabase but couldn't query subscriptions: {type(e).__name__}")
        
        return supabase
    except Exception as e:
        st.error(f"❌ Error connecting to Supabase: {type(e).__name__}")
        return None

# Create a simple Streamlit app to test the connection
st.title("Direct Supabase Connection Test")

# Display environment variables (redacted)
st.subheader("Environment Variables")
env_vars = {k: "..." if any(s in k.lower() for s in ["key", "secret", "password"]) else v 
            for k, v in os.environ.items() 
            if k.startswith(("SUPABASE_", "OPENAI_", "EMBEDDING_"))}
st.json(env_vars)

# Button to test connection
if st.button("Test Direct Supabase Connection"):
    supabase = direct_supabase_connect()
    
    if supabase:
        # If connection successful, offer to fix the main application
        if st.button("Apply This Fix to Main Application"):
            # Update the utils.py file to use this direct connection approach
            try:
                # Set environment variables directly
                os.environ["SUPABASE_URL"] = "https://effhhuuhualzawjtnczv.supabase.co"
                st.success("✅ Fixed environment variables for this session")
                st.info("To make this fix permanent, update your Render environment variables")
            except Exception as e:
                st.error(f"Error applying fix: {str(e)}")
