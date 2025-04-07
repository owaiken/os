import streamlit as st
import os
from utils.license_manager import get_license_manager
import json

def license_tab():
    """
    Streamlit UI tab for license management.
    """
    # Get the license manager
    license_manager = get_license_manager()
    
    # Create columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## License Management")
        st.markdown("""
        Owaiken uses [Keygen.sh](https://keygen.sh) for license management. 
        You'll need to enter your license key to use this application.
        """)
        
        # Check if Keygen credentials are configured
        if not license_manager.account_id or not license_manager.product_id:
            st.warning("⚠️ Keygen account and product ID are not configured. Please set them in the Environment tab.")
            
            # Show configuration form
            with st.expander("Configure Keygen Credentials"):
                account_id = st.text_input("Keygen Account ID", value=license_manager.account_id or "")
                product_id = st.text_input("Keygen Product ID", value=license_manager.product_id or "")
                
                if st.button("Save Keygen Configuration"):
                    # Update environment variables
                    env_file_path = os.path.join("workbench", "env_vars.json")
                    try:
                        # Load existing env vars
                        if os.path.exists(env_file_path):
                            with open(env_file_path, "r") as f:
                                env_vars = json.load(f)
                        else:
                            env_vars = {}
                        
                        # Update with new values
                        env_vars["KEYGEN_ACCOUNT_ID"] = account_id
                        env_vars["KEYGEN_PRODUCT_ID"] = product_id
                        
                        # Save back to file
                        os.makedirs(os.path.dirname(env_file_path), exist_ok=True)
                        with open(env_file_path, "w") as f:
                            json.dump(env_vars, f, indent=2)
                            
                        # Update license manager
                        license_manager.account_id = account_id
                        license_manager.product_id = product_id
                        
                        st.success("✅ Keygen configuration saved successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error saving configuration: {str(e)}")
        
        # Check if a license is already activated
        existing_license = license_manager._load_saved_license()
        
        if existing_license:
            st.info(f"🔑 License key found: {existing_license[:5]}...{existing_license[-5:]}")
            
            # Validate the license
            if st.button("Validate License"):
                with st.spinner("Validating license..."):
                    result = license_manager.validate_license()
                    
                if result["valid"]:
                    st.success(f"✅ {result['message']}")
                    
                    # Show license details if available
                    if "data" in result:
                        license_data = result["data"]
                        expiry = license_data.get("meta", {}).get("expiry")
                        if expiry:
                            st.info(f"📅 License expires on: {expiry}")
                else:
                    st.error(f"❌ {result['message']}")
                    
                    # If license is invalid, allow entering a new one
                    st.warning("Please enter a new license key below.")
                    existing_license = None
                    
            if st.button("Remove License"):
                try:
                    os.remove(license_manager.license_file_path)
                    st.success("✅ License removed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error removing license: {str(e)}")
        
        # Show license activation form if no valid license is found
        if not existing_license:
            # Add CSS to ensure text is black on white theme
            st.markdown("""
            <style>
            /* Ensure text is black on white theme */
            .light-mode p, .light-mode h1, .light-mode h2, .light-mode h3, .light-mode h4, .light-mode h5, .light-mode h6, .light-mode span, .light-mode div {
                color: black !important;
            }
            
            /* Apply specific styling to the activation header */
            .activate-license-header {
                color: black !important;
                font-size: 1.5rem !important;
                font-weight: bold !important;
                margin-bottom: 1rem !important;
            }
            </style>
            
            <div class="activate-license-header">Activate License</div>
            """, unsafe_allow_html=True)
            # Add custom CSS to make the input field completely transparent with styling
            st.markdown("""
            <style>
            /* Target the specific input field */
            div[data-testid="stTextInput"] > div > div > input {
                background-color: transparent !important;
                border: 1px solid rgba(128, 128, 128, 0.4) !important;
                color: var(--text-color) !important;
            }
            /* Override any parent container backgrounds */
            div[data-testid="stTextInput"] > div > div {
                background-color: transparent !important;
            }
            div[data-testid="stTextInput"] > div {
                background-color: transparent !important;
            }
            div[data-testid="stTextInput"] {
                background-color: transparent !important;
            }
            /* Make sure the placeholder text is visible */
            div[data-testid="stTextInput"] > div > div > input::placeholder {
                color: rgba(128, 128, 128, 0.6) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Use a Keygen.sh style placeholder (XXXX-XXXX-XXXX-XXXX)
            license_key = st.text_input("Enter your license key", type="password", placeholder="XXXX-XXXX-XXXX-XXXX")
            
            if st.button("Activate License"):
                if not license_key:
                    st.error("❌ Please enter a license key.")
                else:
                    with st.spinner("Activating license..."):
                        result = license_manager.activate_license(license_key)
                        
                    if result["success"]:
                        st.success(f"✅ {result['message']}")
                        st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
    
    with col2:
        st.markdown("## License Information")
        st.markdown("""
        ### About Licensing
        
        Licensing ensures:
        - Authorized usage
        - Access to updates
        - Technical support
        
        ### License Types
        
        - **Trial**: Limited time evaluation
        - **Standard**: Single user license
        - **Team**: Multiple users in one organization
        - **Enterprise**: Custom deployment with priority support
        
        ### Need a License?
        
        Visit our website to purchase a license or contact sales for volume discounts.
        """)
        
        # Display machine fingerprint for troubleshooting
        with st.expander("Technical Information"):
            st.code(license_manager.machine_fingerprint, language="text")
            st.caption("Machine Fingerprint (used for license activation)")
