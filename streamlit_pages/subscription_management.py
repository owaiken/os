"""
Subscription Management Page for Owaiken
Handles user subscriptions, payments, and license management
"""
import streamlit as st
import os
import json
import uuid
import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
from streamlit_pages.auth_system import (
    get_current_user, 
    check_subscription,
    create_subscription,
    display_login_ui,
    display_subscription_ui,
    auth_required
)

def generate_license_key(user_id, plan, expires_at):
    """Generate a license key for downloadable version"""
    # Create a unique license key based on user ID and plan
    license_key = f"OWAIKEN-{plan.upper()}-{user_id[:8]}-{uuid.uuid4().hex[:8]}"
    return license_key

def generate_qr_code(data):
    """Generate a QR code for the license key"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def display_license_information(user, subscription):
    """Display license information for the user"""
    st.subheader("Your Owaiken License")
    
    # Generate license key if not already in session
    if "license_key" not in st.session_state:
        st.session_state.license_key = generate_license_key(
            user.get("id"), 
            subscription.get("plan"),
            subscription.get("expires_at")
        )
    
    license_key = st.session_state.license_key
    
    # Display license details
    st.write(f"**License Type:** {subscription.get('plan').capitalize()}")
    st.write(f"**Status:** {'Active' if subscription.get('status') == 'active' else 'Inactive'}")
    st.write(f"**Expires:** {datetime.fromisoformat(subscription.get('expires_at')).strftime('%B %d, %Y')}")
    
    # Display license key
    st.code(license_key, language=None)
    
    # Generate QR code for easy scanning
    qr_code = generate_qr_code(json.dumps({
        "license_key": license_key,
        "user_id": user.get("id"),
        "plan": subscription.get("plan"),
        "expires_at": subscription.get("expires_at")
    }))
    
    st.image(f"data:image/png;base64,{qr_code}", caption="Scan to activate desktop app")
    
    # Download options
    st.subheader("Download Owaiken Desktop")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Download for Windows",
            data=b"Placeholder for Windows installer",  # Replace with actual installer
            file_name="owaiken_installer_windows.exe",
            mime="application/octet-stream",
            disabled=True  # Enable when installer is available
        )
        st.caption("Coming soon")
    
    with col2:
        st.download_button(
            label="Download for Mac",
            data=b"Placeholder for Mac installer",  # Replace with actual installer
            file_name="owaiken_installer_mac.dmg",
            mime="application/octet-stream",
            disabled=True  # Enable when installer is available
        )
        st.caption("Coming soon")
    
    # Installation instructions
    with st.expander("Installation Instructions"):
        st.write("""
        1. Download the installer for your operating system
        2. Run the installer and follow the on-screen instructions
        3. Launch Owaiken Desktop
        4. When prompted, enter your license key or scan the QR code above
        5. Enjoy all the features of Owaiken on your desktop!
        """)

def display_subscription_management(user, subscription):
    """Display subscription management options"""
    st.subheader("Manage Your Subscription")
    
    # Display current plan
    st.write(f"**Current Plan:** {subscription.get('plan').capitalize()}")
    st.write(f"**Status:** {'Active' if subscription.get('status') == 'active' else 'Inactive'}")
    st.write(f"**Renewal Date:** {datetime.fromisoformat(subscription.get('expires_at')).strftime('%B %d, %Y')}")
    
    # Plan upgrade/downgrade options
    if subscription.get("plan") == "monthly":
        st.write("### Upgrade to Annual Plan")
        st.write("Save 16% by switching to our annual plan!")
        
        if st.button("Upgrade to Annual Plan"):
            # In demo mode, create a new annual subscription
            new_subscription = create_subscription(
                user.get("id"),
                "annual",
                "upgrade_" + str(uuid.uuid4()),
                9999
            )
            
            if new_subscription:
                st.success("Upgraded to annual plan successfully!")
                st.session_state.pop("license_key", None)  # Reset license key
                st.rerun()
    
    elif subscription.get("plan") == "annual":
        st.write("### Switch to Monthly Plan")
        st.write("You're currently on our best value plan!")
        
        if st.button("Switch to Monthly Plan"):
            # In demo mode, create a new monthly subscription
            new_subscription = create_subscription(
                user.get("id"),
                "monthly",
                "downgrade_" + str(uuid.uuid4()),
                999
            )
            
            if new_subscription:
                st.success("Switched to monthly plan successfully!")
                st.session_state.pop("license_key", None)  # Reset license key
                st.rerun()
    
    # Cancellation option
    with st.expander("Cancel Subscription"):
        st.write("We're sorry to see you go! Your subscription will remain active until the end of your billing period.")
        
        if st.button("Cancel Subscription", key="cancel_subscription"):
            # In demo mode, just mark the subscription as cancelled
            st.warning("Your subscription has been cancelled. You will have access until the end of your billing period.")
            # In a real implementation, we would update the subscription status in the database

@auth_required
def subscription_tab(user):
    """Main subscription management tab"""
    st.title("Owaiken Subscription")
    
    # Check if user has a subscription
    subscription = check_subscription(user.get("id"))
    
    if subscription:
        # User has an active subscription
        tab1, tab2 = st.tabs(["License Information", "Manage Subscription"])
        
        with tab1:
            display_license_information(user, subscription)
        
        with tab2:
            display_subscription_management(user, subscription)
    else:
        # User doesn't have a subscription
        st.write("### Get Started with Owaiken")
        st.write("Choose a subscription plan to access all features of Owaiken, including the desktop application.")
        
        display_subscription_ui(user)

def subscription_page():
    """Entry point for subscription page"""
    # Get current user
    user = get_current_user()
    
    if user:
        subscription_tab(user)
    else:
        st.title("Owaiken Subscription")
        st.write("Please log in to manage your subscription.")
        display_login_ui()
