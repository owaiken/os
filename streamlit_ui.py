from __future__ import annotations
from dotenv import load_dotenv
import streamlit as st
import logfire
import asyncio
import os
import secrets
import stat
from utils.license_manager import get_license_manager

# Set page config - must be the first Streamlit command
try:
    st.set_page_config(
        page_title="Owaiken - Agent Builder",
        page_icon="public/favicon.ico",
        layout="wide",
    )
except:
    # Fallback if favicon is not available
    st.set_page_config(
        page_title="Owaiken - Agent Builder",
        layout="wide",
    )

# Utilities and styles
from utils.utils import get_clients
from streamlit_pages.styles import load_css
from streamlit_pages.sidebar_theme import apply_sidebar_theme
from streamlit_pages.green_to_blue import change_green_to_blue
from streamlit_pages.direct_css_override import apply_direct_css_override

# Streamlit pages
from streamlit_pages.intro import intro_tab
from streamlit_pages.chat import chat_tab
from streamlit_pages.environment import environment_tab
from streamlit_pages.database import database_tab
from streamlit_pages.documentation import documentation_tab
from streamlit_pages.agent_service import agent_service_tab
from streamlit_pages.mcp import mcp_tab
from streamlit_pages.future_enhancements import future_enhancements_tab
from streamlit_pages.license import license_tab
from streamlit_pages.theme_selector import theme_selector
from streamlit_pages.ui_components import ui_components_tab
from streamlit_pages.n8n_integration import n8n_integration_tab, n8n_knowledge_base
from streamlit_pages.logo_uploader import logo_uploader_tab
from streamlit_pages.openmanus_integration import openmanus_tab as owaiken_os_tab
from streamlit_pages.subscription_management import subscription_page
from streamlit_pages.auth_system import initialize_auth_system, get_current_user

# Load environment variables from .env file
load_dotenv()

# Function to securely create the secrets file with proper permissions
def create_secure_secrets_file():
    secrets_dir = ".streamlit"
    secrets_file = os.path.join(secrets_dir, "secrets.toml")
    
    # Create directory with restricted permissions (700 - only owner can access)
    if not os.path.exists(secrets_dir):
        os.makedirs(secrets_dir, exist_ok=True)
        # Set directory permissions to be restricted (rwx-----)
        try:
            os.chmod(secrets_dir, stat.S_IRWXU)
        except Exception as e:
            print(f"Warning: Could not set permissions on secrets directory: {type(e).__name__}")
    
    # Only create the file if it doesn't exist (don't overwrite existing secrets)
    if not os.path.exists(secrets_file):
        with open(secrets_file, "w") as f:
            f.write("# Owaiken Secrets Configuration\n")
            f.write("# SECURITY WARNING: Store actual API keys in environment variables for production\n")
            f.write("# This file should only be used for development purposes\n\n")
            f.write("# OpenAI API Key (for Whisper and other OpenAI services)\n")
            f.write("OPENAI_API_KEY = \"\"\n\n")
            f.write("# Supabase Configuration (if needed)\n")
            f.write("SUPABASE_URL = \"\"\n")
            f.write("SUPABASE_KEY = \"\"\n\n")
            f.write("# Keygen License Configuration\n")
            f.write("KEYGEN_ACCOUNT_ID = \"\"\n")
            f.write("KEYGEN_PRODUCT_ID = \"\"\n")
            f.write("\n# Security settings\n")
            # Generate a random cookie password for session security
            f.write(f"COOKIE_PASSWORD = \"{secrets.token_hex(32)}\"\n")
        
        # Set file permissions to be restricted (rw-------)
        try:
            os.chmod(secrets_file, stat.S_IRUSR | stat.S_IWUSR)
        except Exception as e:
            print(f"Warning: Could not set permissions on secrets file: {type(e).__name__}")

# Create secure secrets file
try:
    create_secure_secrets_file()
except Exception as e:
    print(f"Warning: Could not create secrets file: {type(e).__name__}")

# Initialize clients safely
try:
    # Initialize clients
    openai_client, supabase = get_clients()
except Exception as e:
    st.warning(f"Warning: Could not initialize some clients. Error: {str(e)}")
    openai_client, supabase = None, None

# Load custom CSS styles
load_css()

# Apply sidebar theme
apply_sidebar_theme()

# Change green text to blue
change_green_to_blue()

# Apply direct CSS override
apply_direct_css_override()

# Configure logfire to suppress warnings (optional)
logfire.configure(send_to_logfire='never')

async def main():
    try:
        # Initialize authentication system
        user = initialize_auth_system()
        
        # Check if license is valid
        license_manager = get_license_manager()
        license_valid = False
        
        # Check for existing license
        if license_manager._load_saved_license():
            validation = license_manager.validate_license()
            license_valid = validation.get("valid", False)
        
        # Initialize license validity in session state
        if "license_valid" not in st.session_state:
            st.session_state.license_valid = license_valid
        
        # Check for theme in query parameters
        query_params = st.query_params
        if "theme" in query_params:
            theme = query_params["theme"]
            if theme in ["light", "dark"]:
                # Apply theme setting
                st.session_state.theme = theme
                # This is a workaround since Streamlit doesn't allow direct theme changing
                # The actual theme change happens on page reload with the query parameter
        
        # Check for tab query parameter
        if "tab" in query_params:
            tab_name = query_params["tab"]
            if tab_name in ["Intro", "Chat", "Environment", "Database", "Documentation", "Agent Service", "MCP", "Future Enhancements", "License", "UI Components"]:
                st.session_state.selected_tab = tab_name

        # Add sidebar navigation
        with st.sidebar:
            # Check if logo files exist in the public directory
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            public_dir = os.path.join(current_dir, "public")
            
            light_logo_path = None
            dark_logo_path = None
            
            # Check for SVG logos first
            if os.path.exists(os.path.join(public_dir, "Owaiken_Black.svg")):
                light_logo_path = os.path.join(public_dir, "Owaiken_Black.svg")
            elif os.path.exists(os.path.join(public_dir, "Owaiken_Black.png")):
                light_logo_path = os.path.join(public_dir, "Owaiken_Black.png")
                
            if os.path.exists(os.path.join(public_dir, "Owaiken_White.svg")):
                dark_logo_path = os.path.join(public_dir, "Owaiken_White.svg")
            elif os.path.exists(os.path.join(public_dir, "Owaiken_White.png")):
                dark_logo_path = os.path.join(public_dir, "Owaiken_White.png")
            
            # Display the appropriate logo based on the current theme
            if st.get_option("theme.base") == "light":
                if light_logo_path and os.path.getsize(light_logo_path) > 10:  # Make sure file is not empty
                    try:
                        st.image(light_logo_path, width=250)
                    except Exception as e:
                        st.error(f"Error loading logo: {str(e)}")
                        from streamlit_pages.logo_handler import display_logo
                        display_logo(logo_type="light")
                else:
                    from streamlit_pages.logo_handler import display_logo
                    display_logo(logo_type="light")
            else:
                if dark_logo_path and os.path.getsize(dark_logo_path) > 10:  # Make sure file is not empty
                    try:
                        st.image(dark_logo_path, width=250)
                    except Exception as e:
                        st.error(f"Error loading logo: {str(e)}")
                        from streamlit_pages.logo_handler import display_logo
                        display_logo(logo_type="dark")
                else:
                    from streamlit_pages.logo_handler import display_logo
                    display_logo(logo_type="dark")
                
            # Add theme selector
            with st.expander("Theme Settings"):
                theme_selector()
            
            # Navigation options with vertical buttons
            st.write("### Navigation")
            
            # Initialize session state for selected tab if not present
            if "selected_tab" not in st.session_state:
                st.session_state.selected_tab = "Intro"
            
            # Initialize other session state variables
            if "show_all_components" not in st.session_state:
                st.session_state.show_all_components = False
            
            # Display user info if logged in
            user = get_current_user()
            if user:
                st.write(f"Logged in as: {user.get('firstName', '')} {user.get('lastName', '')}")
                st.button("Logout", key="logout_button", on_click=lambda: st.session_state.pop("clerk_token", None))
            
            # Vertical navigation buttons
            owaiken_os_button = st.button("Owaiken OS", use_container_width=True, key="owaiken_os_button")
            subscription_button = st.button("Subscription", use_container_width=True, key="subscription_button")
            license_button = st.button("License", use_container_width=True, key="license_button")
            intro_button = st.button("Intro", use_container_width=True, key="intro_button")
            chat_button = st.button("Chat", use_container_width=True, key="chat_button")
            env_button = st.button("Environment", use_container_width=True, key="env_button")
            db_button = st.button("Database", use_container_width=True, key="db_button")
            docs_button = st.button("Documentation", use_container_width=True, key="docs_button")
            service_button = st.button("Agent Service", use_container_width=True, key="service_button")
            mcp_button = st.button("MCP", use_container_width=True, key="mcp_button")
            ui_components_button = st.button("UI Components", use_container_width=True, key="ui_components_button")
            n8n_button = st.button("N8N Integration", use_container_width=True, key="n8n_button")
            n8n_kb_button = st.button("N8N Knowledge Base", use_container_width=True, key="n8n_kb_button")
            logo_uploader_button = st.button("Logo Uploader", use_container_width=True, key="logo_uploader_button")
            future_enhancements_button = st.button("Future Enhancements", use_container_width=True, key="future_enhancements_button")
            
            # Update selected tab based on button clicks
            if owaiken_os_button:
                st.session_state.selected_tab = "Owaiken OS"
            elif subscription_button:
                st.session_state.selected_tab = "Subscription"
            elif license_button:
                st.session_state.selected_tab = "License"
            elif intro_button:
                st.session_state.selected_tab = "Intro"
            elif chat_button:
                st.session_state.selected_tab = "Chat"
            elif mcp_button:
                st.session_state.selected_tab = "MCP"
            elif env_button:
                st.session_state.selected_tab = "Environment"
            elif service_button:
                st.session_state.selected_tab = "Agent Service"
            elif db_button:
                st.session_state.selected_tab = "Database"
            elif docs_button:
                st.session_state.selected_tab = "Documentation"
            elif ui_components_button:
                st.session_state.selected_tab = "UI Components"
            elif n8n_button:
                st.session_state.selected_tab = "N8N Integration"
            elif n8n_kb_button:
                st.session_state.selected_tab = "N8N Knowledge Base"
            elif logo_uploader_button:
                st.session_state.selected_tab = "Logo Uploader"
            elif future_enhancements_button:
                st.session_state.selected_tab = "Future Enhancements"
        
        # Display the selected tab - allow access to all features for development/testing
        if st.session_state.selected_tab == "License":
            st.title("Owaiken - License Management")
            license_tab()
            # Check if license was just validated
            if st.session_state.get("license_valid", False) != license_valid:
                st.session_state.license_valid = license_valid
                st.rerun()
        elif st.session_state.selected_tab == "Intro":
            st.title("Owaiken - Introduction")
            intro_tab()
        elif st.session_state.selected_tab == "Chat":
            st.title("Owaiken - Agent Builder")
            await chat_tab()
        elif st.session_state.selected_tab == "MCP":
            st.title("Owaiken - MCP Configuration")
            mcp_tab()
        elif st.session_state.selected_tab == "Environment":
            st.title("Owaiken - Environment Configuration")
            environment_tab()
        elif st.session_state.selected_tab == "Agent Service":
            st.title("Owaiken - Agent Service")
            agent_service_tab()
        elif st.session_state.selected_tab == "Database":
            st.title("Owaiken - Database Configuration")
            database_tab(supabase)
        elif st.session_state.selected_tab == "Documentation":
            st.title("Owaiken - Documentation")
            documentation_tab(supabase)
        elif st.session_state.selected_tab == "UI Components":
            st.title("Owaiken - UI Components")
            ui_components_tab()
        elif st.session_state.selected_tab == "Future Enhancements":
            st.title("Owaiken - Future Enhancements")
            future_enhancements_tab()
        elif st.session_state.selected_tab == "N8N Integration":
            st.title("Owaiken - N8N Workflow Integration")
            n8n_integration_tab()
        elif st.session_state.selected_tab == "N8N Knowledge Base":
            st.title("Owaiken - N8N Knowledge Base")
            n8n_knowledge_base()
        elif st.session_state.selected_tab == "Owaiken OS":
            st.title("Owaiken OS")
            owaiken_os_tab()
        elif st.session_state.selected_tab == "Subscription":
            st.title("Owaiken - Subscription Management")
            subscription_page()
        elif st.session_state.selected_tab == "Logo Uploader":
            st.title("Owaiken - Logo Uploader")
            logo_uploader_tab()
        
        # Add a gentle reminder if no license is present (instead of blocking access)
        if not license_valid and st.session_state.selected_tab != "License":
            st.sidebar.info("💡 You're currently using Owaiken in evaluation mode. For full functionality, please activate your license.")
    
    except Exception as e:
        # Handle any exceptions in the main app flow
        st.error("The application encountered an issue. You can continue using it in limited mode.")
        print(f"Application error: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        st.error("The application could not start properly. Please check your configuration.")
        print(f"Fatal error: {type(e).__name__}: {str(e)}")
