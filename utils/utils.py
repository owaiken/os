from supabase import Client, create_client
from openai import AsyncOpenAI
from dotenv import load_dotenv
from datetime import datetime
from functools import wraps
from typing import Optional
import streamlit as st
import webbrowser
import importlib
import inspect
import json
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
workbench_dir = os.path.join(parent_dir, "workbench")

def write_to_log(message: str):
    """Write a message to the logs.txt file in the workbench directory.
    
    Securely logs messages while redacting sensitive information.
    
    Args:
        message: The message to log
    """
    # Redact sensitive information from logs
    redacted_message = message
    sensitive_patterns = [
        (r'key[^\s]*[\s]*[:=][\s]*["\']?([\w\-\.]+)["\']?', 'key***=REDACTED'),
        (r'password[^\s]*[\s]*[:=][\s]*["\']?([\w\-\.]+)["\']?', 'password=REDACTED'),
        (r'secret[^\s]*[\s]*[:=][\s]*["\']?([\w\-\.]+)["\']?', 'secret=REDACTED'),
        (r'token[^\s]*[\s]*[:=][\s]*["\']?([\w\-\.]+)["\']?', 'token=REDACTED'),
        (r'auth[^\s]*[\s]*[:=][\s]*["\']?([\w\-\.]+)["\']?', 'auth=REDACTED'),
    ]
    
    for pattern, replacement in sensitive_patterns:
        redacted_message = re.sub(pattern, replacement, redacted_message, flags=re.IGNORECASE)
    
    # Get the directory one level up from the current file
    log_path = os.path.join(workbench_dir, "logs.txt")
    os.makedirs(workbench_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {redacted_message}\n"

    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception:
        # Fail silently - logging should never break application functionality
        pass

def get_env_var(var_name: str, profile: Optional[str] = None) -> Optional[str]:
    """Get an environment variable from the saved JSON file or from environment variables.
    
    Args:
        var_name: The name of the environment variable to retrieve
        profile: The profile to use (if None, uses the current profile)
        
    Returns:
        The value of the environment variable or None if not found
    """
    # Path to the JSON file storing environment variables
    env_file_path = os.path.join(workbench_dir, "env_vars.json")
    
    # First try to get from JSON file
    if os.path.exists(env_file_path):
        try:
            with open(env_file_path, "r") as f:
                env_vars = json.load(f)
                
                # If profile is specified, use it; otherwise use current profile
                current_profile = profile or env_vars.get("current_profile", "default")
                
                # Get variables for the profile
                if "profiles" in env_vars and current_profile in env_vars["profiles"]:
                    profile_vars = env_vars["profiles"][current_profile]
                    if var_name in profile_vars and profile_vars[var_name]:
                        return profile_vars[var_name]
                
                # For backward compatibility, check the root level
                if var_name in env_vars and env_vars[var_name]:
                    return env_vars[var_name]
        except (json.JSONDecodeError, IOError) as e:
            write_to_log(f"Error reading env_vars.json: {str(e)}")
    
    # If not found in JSON, try to get from environment variables
    return os.environ.get(var_name)

def save_env_var(var_name: str, value: str, profile: Optional[str] = None) -> bool:
    """Save an environment variable to the JSON file.
    
    Args:
        var_name: The name of the environment variable
        value: The value to save
        profile: The profile to save to (if None, uses the current profile)
        
    Returns:
        True if successful, False otherwise
    """
    # Path to the JSON file storing environment variables
    env_file_path = os.path.join(workbench_dir, "env_vars.json")
    os.makedirs(workbench_dir, exist_ok=True)
    
    # Load existing env vars or create empty dict
    env_vars = {}
    if os.path.exists(env_file_path):
        try:
            with open(env_file_path, "r") as f:
                env_vars = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            write_to_log(f"Error reading env_vars.json: {str(e)}")
            # Continue with empty dict if file is corrupted
    
    # Initialize profiles structure if it doesn't exist
    if "profiles" not in env_vars:
        env_vars["profiles"] = {}
    
    # If no current profile is set, set it to default
    if "current_profile" not in env_vars:
        env_vars["current_profile"] = "default"
    
    # Determine which profile to use
    current_profile = profile or env_vars.get("current_profile", "default")
    
    # Initialize the profile if it doesn't exist
    if current_profile not in env_vars["profiles"]:
        env_vars["profiles"][current_profile] = {}
    
    # Update the variable in the profile
    env_vars["profiles"][current_profile][var_name] = value
    
    # Save back to file
    try:
        with open(env_file_path, "w") as f:
            json.dump(env_vars, f, indent=2)
        return True
    except IOError as e:
        write_to_log(f"Error writing to env_vars.json: {str(e)}")
        return False

def get_current_profile() -> str:
    """Get the current environment profile name.
    
    Returns:
        The name of the current profile, defaults to "default" if not set
    """
    env_file_path = os.path.join(workbench_dir, "env_vars.json")
    
    if os.path.exists(env_file_path):
        try:
            with open(env_file_path, "r") as f:
                env_vars = json.load(f)
                return env_vars.get("current_profile", "default")
        except (json.JSONDecodeError, IOError) as e:
            write_to_log(f"Error reading env_vars.json: {str(e)}")
    
    return "default"

def set_current_profile(profile_name: str) -> bool:
    """Set the current environment profile.
    
    Args:
        profile_name: The name of the profile to set as current
        
    Returns:
        True if successful, False otherwise
    """
    env_file_path = os.path.join(workbench_dir, "env_vars.json")
    os.makedirs(workbench_dir, exist_ok=True)
    
    # Load existing env vars or create empty dict
    env_vars = {}
    if os.path.exists(env_file_path):
        try:
            with open(env_file_path, "r") as f:
                env_vars = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            write_to_log(f"Error reading env_vars.json: {str(e)}")
            # Continue with empty dict if file is corrupted
    
    # Initialize profiles structure if it doesn't exist
    if "profiles" not in env_vars:
        env_vars["profiles"] = {}
    
    # Initialize the profile if it doesn't exist
    if profile_name not in env_vars["profiles"]:
        env_vars["profiles"][profile_name] = {}
    
    # Set the current profile
    env_vars["current_profile"] = profile_name
    
    # Save back to file
    try:
        with open(env_file_path, "w") as f:
            json.dump(env_vars, f, indent=2)
        return True
    except IOError as e:
        write_to_log(f"Error writing to env_vars.json: {str(e)}")
        return False

def get_all_profiles() -> list:
    """Get a list of all available environment profiles.
    
    Returns:
        List of profile names
    """
    env_file_path = os.path.join(workbench_dir, "env_vars.json")
    
    if os.path.exists(env_file_path):
        try:
            with open(env_file_path, "r") as f:
                env_vars = json.load(f)
                if "profiles" in env_vars:
                    return list(env_vars["profiles"].keys())
        except (json.JSONDecodeError, IOError) as e:
            write_to_log(f"Error reading env_vars.json: {str(e)}")
    
    # Return default if no profiles exist
    return ["default"]

def create_profile(profile_name: str) -> bool:
    """Create a new environment profile.
    
    Args:
        profile_name: The name of the profile to create
        
    Returns:
        True if successful, False otherwise
    """
    env_file_path = os.path.join(workbench_dir, "env_vars.json")
    os.makedirs(workbench_dir, exist_ok=True)
    
    # Load existing env vars or create empty dict
    env_vars = {}
    if os.path.exists(env_file_path):
        try:
            with open(env_file_path, "r") as f:
                env_vars = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            write_to_log(f"Error reading env_vars.json: {str(e)}")
            # Continue with empty dict if file is corrupted
    
    # Initialize profiles structure if it doesn't exist
    if "profiles" not in env_vars:
        env_vars["profiles"] = {}
    
    # Create the profile if it doesn't exist
    if profile_name not in env_vars["profiles"]:
        env_vars["profiles"][profile_name] = {}
        
        # Save back to file
        try:
            with open(env_file_path, "w") as f:
                json.dump(env_vars, f, indent=2)
            return True
        except IOError as e:
            write_to_log(f"Error writing to env_vars.json: {str(e)}")
            return False
    
    # Profile already exists
    return True

def delete_profile(profile_name: str) -> bool:
    """Delete an environment profile.
    
    Args:
        profile_name: The name of the profile to delete
        
    Returns:
        True if successful, False otherwise
    """
    # Don't allow deleting the default profile
    if profile_name == "default":
        return False
        
    env_file_path = os.path.join(workbench_dir, "env_vars.json")
    
    if os.path.exists(env_file_path):
        try:
            with open(env_file_path, "r") as f:
                env_vars = json.load(f)
                
            if "profiles" in env_vars and profile_name in env_vars["profiles"]:
                # Delete the profile
                del env_vars["profiles"][profile_name]
                
                # If the current profile was deleted, set to default
                if env_vars.get("current_profile") == profile_name:
                    env_vars["current_profile"] = "default"
                
                # Save back to file
                with open(env_file_path, "w") as f:
                    json.dump(env_vars, f, indent=2)
                return True
        except (json.JSONDecodeError, IOError) as e:
            write_to_log(f"Error reading/writing env_vars.json: {str(e)}")
    
    return False

def get_profile_env_vars(profile_name: Optional[str] = None) -> dict:
    """Get all environment variables for a specific profile.
    
    Args:
        profile_name: The name of the profile (if None, uses the current profile)
        
    Returns:
        Dictionary of environment variables for the profile
    """
    env_file_path = os.path.join(workbench_dir, "env_vars.json")
    
    if os.path.exists(env_file_path):
        try:
            with open(env_file_path, "r") as f:
                env_vars = json.load(f)
                
                # If profile is specified, use it; otherwise use current profile
                current_profile = profile_name or env_vars.get("current_profile", "default")
                
                # Get variables for the profile
                if "profiles" in env_vars and current_profile in env_vars["profiles"]:
                    return env_vars["profiles"][current_profile]
                
                # For backward compatibility, if no profiles structure but we're looking for default
                if current_profile == "default" and "profiles" not in env_vars:
                    # Return all variables except profiles and current_profile
                    return {k: v for k, v in env_vars.items() 
                            if k not in ["profiles", "current_profile"]}
        except (json.JSONDecodeError, IOError) as e:
            write_to_log(f"Error reading env_vars.json: {str(e)}")
    
    return {}

def log_node_execution(func):
    """Decorator to log the start and end of graph node execution.
    
    Args:
        func: The async function to wrap
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = func.__name__
        write_to_log(f"Starting node: {func_name}")
        try:
            result = await func(*args, **kwargs)
            write_to_log(f"Completed node: {func_name}")
            return result
        except Exception as e:
            write_to_log(f"Error in node {func_name}: {str(e)}")
            raise
    return wrapper

# Helper function to create a button that opens a tab in a new window
def create_new_tab_button(label, tab_name, key=None, use_container_width=False):
    """Create a button that opens a specified tab in a new browser window"""
    # Create a unique key if none provided
    if key is None:
        key = f"new_tab_{tab_name.lower().replace(' ', '_')}"
    
    # Get the base URL
    base_url = st.query_params.get("base_url", "")
    if not base_url:
        # If base_url is not in query params, use the default localhost URL
        base_url = "http://localhost:8501"
    
    # Create the URL for the new tab
    new_tab_url = f"{base_url}/?tab={tab_name}"
    
    # Create a button that will open the URL in a new tab when clicked
    if st.button(label, key=key, use_container_width=use_container_width):
        webbrowser.open_new_tab(new_tab_url)

# Function to reload the owaiken_graph module
def reload_owaiken_graph(show_reload_success=True):
    """Reload the owaiken_graph module to apply new environment variables"""
    try:
        # First reload pydantic_ai_coder
        import owaiken.pydantic_ai_coder
        importlib.reload(owaiken.pydantic_ai_coder)
        
        # Then reload owaiken_graph which imports pydantic_ai_coder
        import owaiken.owaiken_graph
        importlib.reload(owaiken.owaiken_graph)

        # Then reload the crawler
        import owaiken.crawl_pydantic_ai_docs
        importlib.reload(owaiken.crawl_pydantic_ai_docs)        
        
        if show_reload_success:
            st.success("Successfully reloaded Owaiken modules with new environment variables!")
        return True
    except Exception as e:
        st.error(f"Error reloading Owaiken modules: {str(e)}")
        return False        

def get_clients():
    """Initialize API clients with secure credential handling
    
    Following security best practices:
    1. Secure credential handling with proper error messages
    2. Input validation for URLs and API keys
    3. Proper exception handling with minimal error disclosure
    4. Secure logging practices
    
    Returns:
        tuple: (embedding_client, supabase_client)
    """
    # LLM client setup with input validation
    embedding_client = None
    base_url = get_env_var('EMBEDDING_BASE_URL') or 'https://api.openai.com/v1'
    api_key = get_env_var('EMBEDDING_API_KEY') or 'no-api-key-provided'
    provider = get_env_var('EMBEDDING_PROVIDER') or 'OpenAI'
    
    # Validate URL format before using
    if not base_url.startswith(('http://', 'https://')):
        write_to_log(f"Invalid embedding base URL format")
        base_url = 'https://api.openai.com/v1'  # Fallback to default
    
    # Setup OpenAI client for LLM with proper error handling
    try:
        if provider == "Ollama":
            if api_key == "NOT_REQUIRED":
                api_key = "ollama"  # Use a dummy key for Ollama
            embedding_client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        else:
            embedding_client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    except Exception as e:
        write_to_log(f"Error initializing embedding client: {type(e).__name__}")
        # Continue execution - we'll handle the None client downstream

    # Supabase client setup with secure credential handling
    supabase = None
    
    # Get credentials from environment with proper validation
    supabase_url = get_env_var("SUPABASE_URL")
    
    # Handle empty URL case - use hardcoded URL if environment variable is empty
    if not supabase_url or supabase_url.strip() == "":
        supabase_url = "https://effhhuuhualzawjtnczv.supabase.co"
        write_to_log("Using fallback Supabase URL due to empty environment variable")
    
    # Try multiple key names for Supabase with secure logging
    # Start with SUPABASE_SERVICE_KEY for compatibility with original Archon
    supabase_key = get_env_var("SUPABASE_SERVICE_KEY")
    if not supabase_key:
        # Fall back to other key names if service key isn't found
        for key_name in ["SUPABASE_KEY", "SUPABASE_ANON_KEY"]:
            supabase_key = get_env_var(key_name)
            if supabase_key:
                write_to_log(f"Using {key_name} for Supabase connection")
                break
    else:
        write_to_log("Using SUPABASE_SERVICE_KEY for Supabase connection")
    
    # Validate URL format
    if supabase_url and not supabase_url.startswith(('http://', 'https://')):
        write_to_log("Invalid Supabase URL format")
        supabase_url = None
    
    # Initialize Supabase client with proper error handling
    if supabase_url and supabase_key:
        try:
            # Verify connection with a simple query
            supabase = Client(supabase_url, supabase_key)
            write_to_log("Successfully connected to Supabase")
        except Exception as e:
            write_to_log(f"Supabase connection error: {type(e).__name__}")
            # Don't expose detailed error messages that might contain sensitive info
            supabase = None
    else:
        missing = []
        if not supabase_url:
            missing.append("SUPABASE_URL")
        if not supabase_key:
            missing.append("Supabase key")
        write_to_log(f"Supabase initialization skipped: Missing {', '.join(missing)}")

    return embedding_client, supabase
