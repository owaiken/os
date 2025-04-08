"""
Environment Debugger for Owaiken

This script creates a diagnostic page that will show exactly what environment variables
are available in the Render environment and why Supabase connection is failing.
"""

import os
import json
import sys
import traceback
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import utility functions
try:
    from utils.utils import get_env_var, get_clients
except ImportError as e:
    st.error(f"Error importing utils: {e}")

st.set_page_config(
    page_title="Owaiken - Environment Diagnostics",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Owaiken Environment Diagnostics")
st.write("This page helps diagnose environment and connection issues.")

# Check if running on Render
is_render = "RENDER" in os.environ
st.write(f"Running on Render: **{'Yes' if is_render else 'No'}**")

# Load environment variables
load_dotenv()
st.write("Loaded environment variables from .env file (if it exists)")

# Check for secrets.toml
secrets_path = os.path.join(".streamlit", "secrets.toml")
has_secrets = os.path.exists(secrets_path)
st.write(f"secrets.toml exists: **{'Yes' if has_secrets else 'No'}**")

# Show all environment variables (sanitized)
st.subheader("Environment Variables")

env_vars = {}
for key in os.environ:
    # Skip sensitive values
    if any(sensitive in key.lower() for sensitive in ["key", "secret", "password", "token"]):
        env_vars[key] = "[REDACTED]"
    else:
        env_vars[key] = os.environ[key]

st.json(env_vars)

# Check for Supabase credentials
st.subheader("Supabase Credentials Check")

supabase_vars = {
    "SUPABASE_URL": {"found": False, "source": None},
    "SUPABASE_SERVICE_KEY": {"found": False, "source": None},
    "SUPABASE_KEY": {"found": False, "source": None},
    "SUPABASE_ANON_KEY": {"found": False, "source": None}
}

# Check environment variables
for var_name in supabase_vars:
    if var_name in os.environ:
        supabase_vars[var_name]["found"] = True
        supabase_vars[var_name]["source"] = "Environment Variable"

# Check get_env_var function
try:
    for var_name in supabase_vars:
        value = get_env_var(var_name)
        if value:
            supabase_vars[var_name]["found"] = True
            if supabase_vars[var_name]["source"] is None:
                supabase_vars[var_name]["source"] = "get_env_var function"
except Exception as e:
    st.error(f"Error checking get_env_var: {str(e)}")

# Display results
for var_name, info in supabase_vars.items():
    if info["found"]:
        st.success(f"✅ {var_name}: Found in {info['source']}")
    else:
        st.error(f"❌ {var_name}: Not found")

# Test Supabase connection
st.subheader("Supabase Connection Test")

try:
    openai_client, supabase = get_clients()
    if supabase:
        st.success("✅ Successfully created Supabase client")
        
        # Test a simple query
        try:
            response = supabase.table("subscriptions").select("count").execute()
            st.success(f"✅ Successfully queried subscriptions table: {response.data}")
        except Exception as e:
            st.error(f"❌ Error querying subscriptions table: {str(e)}")
            st.code(traceback.format_exc())
    else:
        st.error("❌ Failed to create Supabase client")
except Exception as e:
    st.error(f"❌ Error in get_clients: {str(e)}")
    st.code(traceback.format_exc())

# Detailed utils.py inspection
st.subheader("utils.py Inspection")

try:
    import inspect
    from utils.utils import get_clients
    
    source_code = inspect.getsource(get_clients)
    st.code(source_code, language="python")
except Exception as e:
    st.error(f"Error inspecting get_clients: {str(e)}")

# Recommendations
st.subheader("Recommendations")

if not any(info["found"] for info in supabase_vars.values()):
    st.warning("""
    No Supabase credentials found. Make sure to:
    1. Add SUPABASE_URL and SUPABASE_SERVICE_KEY to your Render environment variables
    2. Deploy the latest version of the code
    """)
elif supabase_vars["SUPABASE_URL"]["found"] and not any(info["found"] for var_name, info in supabase_vars.items() if var_name != "SUPABASE_URL"):
    st.warning("""
    SUPABASE_URL found but no key variable found. Make sure to:
    1. Add SUPABASE_SERVICE_KEY to your Render environment variables
    2. Deploy the latest version of the code
    """)

# Direct environment variable check
st.subheader("Direct Environment Variable Check")

# Create a form to directly check environment variables
with st.form("check_env_var"):
    var_name = st.text_input("Enter environment variable name to check:", "SUPABASE_SERVICE_KEY")
    submitted = st.form_submit_button("Check Variable")
    
    if submitted:
        # Check directly from os.environ
        if var_name in os.environ:
            st.success(f"✅ {var_name} exists in os.environ")
            if any(sensitive in var_name.lower() for sensitive in ["key", "secret", "password", "token"]):
                st.info(f"Value: [REDACTED]")
            else:
                st.info(f"Value: {os.environ[var_name]}")
        else:
            st.error(f"❌ {var_name} not found in os.environ")
        
        # Check using get_env_var
        try:
            value = get_env_var(var_name)
            if value:
                st.success(f"✅ {var_name} found via get_env_var()")
                if any(sensitive in var_name.lower() for sensitive in ["key", "secret", "password", "token"]):
                    st.info(f"Value: [REDACTED]")
                else:
                    st.info(f"Value: {value}")
            else:
                st.error(f"❌ {var_name} not found via get_env_var()")
        except Exception as e:
            st.error(f"Error checking with get_env_var: {str(e)}")

# Add a section to manually test Supabase connection
st.subheader("Manual Supabase Connection Test")

with st.form("manual_supabase_test"):
    supabase_url = st.text_input("Supabase URL:", "https://effhhuuhualzawjtnczv.supabase.co")
    supabase_key = st.text_input("Supabase Key:", "")
    test_button = st.form_submit_button("Test Connection")
    
    if test_button and supabase_url and supabase_key:
        try:
            from supabase import create_client
            
            # Try direct connection
            client = create_client(supabase_url, supabase_key)
            st.success("✅ Successfully created Supabase client directly")
            
            # Test a simple query
            try:
                response = client.table("subscriptions").select("count").execute()
                st.success(f"✅ Successfully queried subscriptions table: {response.data}")
            except Exception as e:
                st.error(f"❌ Error querying subscriptions table: {str(e)}")
                st.code(traceback.format_exc())
        except Exception as e:
            st.error(f"❌ Error creating Supabase client: {str(e)}")
            st.code(traceback.format_exc())
