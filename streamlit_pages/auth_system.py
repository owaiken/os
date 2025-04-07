"""
Authentication and Subscription Management for Owaiken
Integrates Clerk for authentication and Stripe for payments
"""
import streamlit as st
import os
import json
import uuid
import time
from datetime import datetime, timedelta
import requests
from supabase import create_client, Client
from streamlit_pages.security_config import (
    get_secure_supabase_client,
    SecureQueryBuilder,
    sanitize_input,
    initialize_database_security
)

# Use secure Supabase client
def get_supabase_client():
    """Get secure Supabase client from environment variables or secrets"""
    return get_secure_supabase_client()

# Initialize Clerk client
def get_clerk_token():
    """Get Clerk token from query parameters or session state"""
    # Check for token in query parameters
    query_params = st.query_params
    if "clerk_token" in query_params:
        token = query_params["clerk_token"]
        # Store token in session state
        st.session_state.clerk_token = token
        return token
    
    # Check for token in session state
    if "clerk_token" in st.session_state:
        return st.session_state.clerk_token
    
    return None

def verify_clerk_token(token):
    """Verify Clerk token with Clerk API"""
    if not token:
        return None
    
    clerk_api_key = st.secrets.get("CLERK_SECRET_KEY", os.environ.get("CLERK_SECRET_KEY", ""))
    if not clerk_api_key:
        st.warning("Clerk API key not found. Running in demo mode.")
        # In demo mode, accept any token
        return {"id": "demo_user", "email": "demo@example.com", "firstName": "Demo", "lastName": "User"}
    
    try:
        headers = {
            "Authorization": f"Bearer {clerk_api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            "https://api.clerk.dev/v1/tokens/verify",
            headers=headers,
            params={"token": token}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error verifying token: {str(e)}")
        return None

def get_current_user():
    """Get current user from Clerk token"""
    token = get_clerk_token()
    user_data = verify_clerk_token(token)
    
    if not user_data:
        return None
    
    return user_data

def check_subscription(user_id):
    """Check if user has an active subscription"""
    supabase = get_supabase_client()
    
    if not supabase:
        # In demo mode, return a demo subscription
        return {
            "active": True,
            "plan": "demo",
            "expires_at": (datetime.now() + timedelta(days=7)).isoformat()
        }
    
    try:
        # Use secure query builder to prevent SQL injection
        secure_query = SecureQueryBuilder(supabase, "subscriptions")
        response = secure_query.select("*").eq("user_id", sanitize_input(user_id)).execute()
        subscriptions = response.data
        
        if not subscriptions:
            return None
        
        # Find the active subscription
        active_subscription = None
        for sub in subscriptions:
            if sub.get("status") == "active" and datetime.fromisoformat(sub.get("expires_at")) > datetime.now():
                active_subscription = sub
                break
        
        return active_subscription
    except Exception as e:
        st.error(f"Error checking subscription: {str(e)}")
        return None

def create_subscription(user_id, plan, payment_id, amount):
    """Create a new subscription for user"""
    supabase = get_supabase_client()
    
    if not supabase:
        # In demo mode, return a demo subscription
        return {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "plan": plan,
            "status": "active",
            "payment_id": payment_id,
            "amount": amount,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat()
        }
    
    try:
        # Calculate expiration date (30 days from now)
        expires_at = (datetime.now() + timedelta(days=30)).isoformat()
        
        # Create subscription record with sanitized inputs
        subscription_data = {
            "user_id": sanitize_input(user_id),
            "plan": sanitize_input(plan),
            "status": "active",
            "payment_id": sanitize_input(payment_id),
            "amount": amount,  # Numeric value doesn't need sanitization
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at
        }
        
        # Use secure query builder to prevent SQL injection
        secure_query = SecureQueryBuilder(supabase, "subscriptions")
        response = secure_query.insert(subscription_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Error creating subscription: {str(e)}")
        return None

def auth_required(func):
    """Decorator to require authentication for a function"""
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            st.warning("Please log in to access this feature")
            display_login_ui()
            return None
        return func(user, *args, **kwargs)
    return wrapper

def subscription_required(func):
    """Decorator to require subscription for a function"""
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            st.warning("Please log in to access this feature")
            display_login_ui()
            return None
        
        subscription = check_subscription(user.get("id"))
        if not subscription:
            st.warning("This feature requires a subscription")
            display_subscription_ui(user)
            return None
        
        return func(user, subscription, *args, **kwargs)
    return wrapper

def display_login_ui():
    """Display login UI using Clerk"""
    clerk_publishable_key = st.secrets.get("CLERK_PUBLISHABLE_KEY", os.environ.get("CLERK_PUBLISHABLE_KEY", ""))
    
    if not clerk_publishable_key:
        st.warning("Clerk API key not found. Running in demo mode.")
        # Show a simple demo login form
        with st.form("demo_login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In")
            
            if submit:
                # In demo mode, accept any credentials
                st.session_state.clerk_token = "demo_token"
                st.rerun()
        return
    
    # Display Clerk sign-in component
    st.markdown(f"""
    <div id="clerk-sign-in"></div>
    <script src="https://cdn.jsdelivr.net/npm/@clerk/clerk-js@latest/dist/clerk.browser.js"></script>
    <script>
        const clerk = Clerk('{clerk_publishable_key}');
        clerk.mountSignIn(document.getElementById('clerk-sign-in'));
        
        // Listen for authentication events
        clerk.on('signed-in', (user) => {{
            // Redirect with token
            window.location.href = window.location.pathname + '?clerk_token=' + clerk.session.token;
        }});
    </script>
    """, unsafe_allow_html=True)

def display_subscription_ui(user):
    """Display subscription options using Stripe"""
    stripe_publishable_key = st.secrets.get("STRIPE_PUBLISHABLE_KEY", os.environ.get("STRIPE_PUBLISHABLE_KEY", ""))
    
    if not stripe_publishable_key:
        st.warning("Stripe API key not found. Running in demo mode.")
        # Show a simple demo subscription form
        st.subheader("Subscribe to Owaiken")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Monthly Plan")
            st.write("$9.99/month")
            st.write("- Full access to all features")
            st.write("- Priority support")
            st.write("- Regular updates")
            
            if st.button("Subscribe Monthly"):
                # In demo mode, create a demo subscription
                subscription = create_subscription(user.get("id"), "monthly", "demo_payment", 999)
                if subscription:
                    st.success("Subscription successful!")
                    st.rerun()
        
        with col2:
            st.write("### Annual Plan")
            st.write("$99.99/year")
            st.write("- All monthly features")
            st.write("- 2 months free")
            st.write("- Early access to new features")
            
            if st.button("Subscribe Annually"):
                # In demo mode, create a demo subscription
                subscription = create_subscription(user.get("id"), "annual", "demo_payment", 9999)
                if subscription:
                    st.success("Subscription successful!")
                    st.rerun()
        return
    
    # Display Stripe checkout component
    st.subheader("Subscribe to Owaiken")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Monthly Plan")
        st.write("$9.99/month")
        st.write("- Full access to all features")
        st.write("- Priority support")
        st.write("- Regular updates")
        
        if st.button("Subscribe Monthly"):
            st.markdown(f"""
            <div id="stripe-monthly-checkout"></div>
            <script src="https://js.stripe.com/v3/"></script>
            <script>
                const stripe = Stripe('{stripe_publishable_key}');
                stripe.redirectToCheckout({{
                    lineItems: [{{price: 'price_monthly_id', quantity: 1}}],
                    mode: 'subscription',
                    successUrl: window.location.href + '?payment_success=true&plan=monthly',
                    cancelUrl: window.location.href,
                    customerEmail: '{user.get("email")}'
                }});
            </script>
            """, unsafe_allow_html=True)
    
    with col2:
        st.write("### Annual Plan")
        st.write("$99.99/year")
        st.write("- All monthly features")
        st.write("- 2 months free")
        st.write("- Early access to new features")
        
        if st.button("Subscribe Annually"):
            st.markdown(f"""
            <div id="stripe-annual-checkout"></div>
            <script src="https://js.stripe.com/v3/"></script>
            <script>
                const stripe = Stripe('{stripe_publishable_key}');
                stripe.redirectToCheckout({{
                    lineItems: [{{price: 'price_annual_id', quantity: 1}}],
                    mode: 'subscription',
                    successUrl: window.location.href + '?payment_success=true&plan=annual',
                    cancelUrl: window.location.href,
                    customerEmail: '{user.get("email")}'
                }});
            </script>
            """, unsafe_allow_html=True)

def handle_payment_success():
    """Handle successful payment from Stripe webhook"""
    query_params = st.query_params
    if "payment_success" in query_params and query_params["payment_success"] == "true":
        user = get_current_user()
        if not user:
            return
        
        plan = query_params.get("plan", "monthly")
        amount = 999 if plan == "monthly" else 9999
        
        # Create subscription
        subscription = create_subscription(
            user.get("id"),
            plan,
            "stripe_" + str(uuid.uuid4()),
            amount
        )
        
        if subscription:
            st.success("Subscription successful! You now have access to all features.")
            # Remove query parameters
            time.sleep(2)
            st.query_params.clear()

def initialize_auth_system():
    """Initialize the authentication system with security features"""
    # Initialize database security
    initialize_database_security()
    
    # Handle payment success
    handle_payment_success()
    
    # Check for user in session
    user = get_current_user()
    
    # Initialize session state for auth
    if "auth_initialized" not in st.session_state:
        st.session_state.auth_initialized = True
        
        # Initialize Supabase tables if needed
        supabase = get_supabase_client()
        if supabase:
            try:
                # Check if subscriptions table exists using secure query builder
                secure_query = SecureQueryBuilder(supabase, "subscriptions")
                response = secure_query.select("count").limit(1).execute()
                # If no error, table exists
            except Exception:
                # Create subscriptions table with proper schema for RLS
                supabase.table("subscriptions").create({
                    "id": "uuid primary key default uuid_generate_v4()",
                    "user_id": "text not null",
                    "plan": "text not null",
                    "status": "text not null",
                    "payment_id": "text not null",
                    "amount": "integer not null",
                    "created_at": "timestamp not null default now()",
                    "expires_at": "timestamp not null"
                })
    
    return user
