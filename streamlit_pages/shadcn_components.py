"""
Shadcn UI components for Owaiken.
This module provides modern UI components using the streamlit-shadcn-ui package.
"""
import streamlit as st
from streamlit_shadcn_ui import button, card, input, select, switch, tabs

def shadcn_demo():
    """
    Demo page showing all available Shadcn UI components.
    """
    st.title("Shadcn UI Components")
    
    # Basic components section
    st.header("Basic Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Button examples
        st.subheader("Buttons")
        button("Default Button", variant="default")
        button("Primary Button", variant="primary")
        button("Secondary Button", variant="secondary")
        button("Destructive Button", variant="destructive")
        button("Outline Button", variant="outline")
        button("Ghost Button", variant="ghost")
        button("Link Button", variant="link")
        
        # Input examples
        st.subheader("Input Fields")
        input_value = input("Username", placeholder="Enter your username")
        if input_value:
            st.write(f"You entered: {input_value}")
            
        # Switch examples
        st.subheader("Switches")
        switch_value = switch("Notifications", checked=True)
        st.write(f"Switch state: {switch_value}")
    
    with col2:
        # Select examples
        st.subheader("Select Dropdown")
        options = [
            {"label": "Option 1", "value": "option1"},
            {"label": "Option 2", "value": "option2"},
            {"label": "Option 3", "value": "option3"}
        ]
        selected = select("Choose an option", options=options)
        if selected:
            st.write(f"Selected: {selected}")
            
        # Badge examples (using Streamlit native components instead)
        st.subheader("Badges")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<span style='background-color: #0284c7; color: white; padding: 4px 8px; border-radius: 4px;'>Default</span>", unsafe_allow_html=True)
        with col2:
            st.markdown("<span style='background-color: #6b7280; color: white; padding: 4px 8px; border-radius: 4px;'>Secondary</span>", unsafe_allow_html=True)
        with col3:
            st.markdown("<span style='border: 1px solid #6b7280; color: #6b7280; padding: 4px 8px; border-radius: 4px;'>Outline</span>", unsafe_allow_html=True)
        with col4:
            st.markdown("<span style='background-color: #ef4444; color: white; padding: 4px 8px; border-radius: 4px;'>Destructive</span>", unsafe_allow_html=True)
        
        # Avatar examples (using Streamlit native components instead)
        st.subheader("Avatars")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div style='background-color: #0284c7; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>U</div>", unsafe_allow_html=True)
            st.caption("User")
        with col2:
            st.markdown("<div style='background-color: #6b7280; color: white; width: 40px; height: 40px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>A</div>", unsafe_allow_html=True)
            st.caption("Admin")
    
    # Card component
    st.header("Card Component")
    with card(title="Owaiken Features", description="Explore the powerful features of Owaiken"):
        st.write("Owaiken provides a comprehensive set of tools for building AI agents.")
        button("Learn More", variant="primary")
    
    # Tabs component
    st.header("Tabs Component")
    tab_content = tabs(
        {
            "Account": "Manage your account settings and preferences.",
            "Password": "Change your password and security settings.",
            "API Keys": "Generate and manage your API keys."
        }
    )
    st.write(f"Active tab content: {tab_content}")
    
    # Alert component (using Streamlit native components instead)
    st.header("Alert Components")
    st.info("This is an informational alert.")
    st.success("Success! Your changes have been saved.")
    st.warning("Warning: This action cannot be undone.")
    st.error("Error: Something went wrong.")
    
    # Notification examples (using Streamlit native components instead)
    st.header("Notifications")
    if button("Show Success Notification", variant="primary"):
        st.success("Operation completed successfully.")
    
    if button("Show Error Notification", variant="destructive"):
        st.error("Something went wrong.")

def shadcn_button(label, variant="default", icon=None, on_click=None):
    """
    Enhanced Shadcn button with icon support.
    
    Args:
        label: Button text
        variant: Button style variant
        icon: Optional icon to display
        on_click: Optional callback function
    
    Returns:
        bool: True if button was clicked
    """
    if icon:
        label = f"{icon} {label}"
    
    clicked = button(label, variant=variant)
    
    if clicked and on_click:
        on_click()
    
    return clicked

def shadcn_card_section(title, content, actions=None):
    """
    Creates a card section with title, content and optional action buttons.
    
    Args:
        title: Card title
        content: Card content (string or callable)
        actions: List of dictionaries with 'label' and 'on_click' keys
    """
    with card(title=title):
        if callable(content):
            content()
        else:
            st.write(content)
            
        if actions:
            cols = st.columns(len(actions))
            for i, action in enumerate(actions):
                with cols[i]:
                    if button(action.get('label', 'Action'), variant=action.get('variant', 'primary')):
                        if action.get('on_click'):
                            # Use a simple function call instead of the toast component
                            if action.get('label') == "Primary Action":
                                st.success("Primary action clicked")
                            elif action.get('label') == "Secondary Action":
                                st.info("Secondary action clicked")
                            else:
                                action['on_click']()

def shadcn_form(fields, submit_label="Submit", on_submit=None):
    """
    Creates a form with Shadcn UI components.
    
    Args:
        fields: List of dictionaries with field configurations
        submit_label: Label for the submit button
        on_submit: Function to call on form submission
        
    Returns:
        dict: Form values if submitted, None otherwise
    """
    form_values = {}
    
    for field in fields:
        field_type = field.get('type', 'input')
        field_id = field.get('id', '')
        label = field.get('label', '')
        
        if field_type == 'input':
            form_values[field_id] = input(
                label, 
                placeholder=field.get('placeholder', ''),
                type=field.get('input_type', 'text')
            )
        elif field_type == 'select':
            form_values[field_id] = select(
                label,
                options=field.get('options', []),
                placeholder=field.get('placeholder', 'Select an option')
            )
        elif field_type == 'switch':
            form_values[field_id] = switch(
                label,
                checked=field.get('default', False)
            )
    
    submitted = button(submit_label, variant="primary")
    
    if submitted:
        if on_submit:
            on_submit(form_values)
        return form_values
    
    return None
