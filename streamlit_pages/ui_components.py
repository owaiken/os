"""
UI Components page for Owaiken.
This page showcases the Shadcn UI components available in the application.
"""
import streamlit as st
from streamlit_shadcn_ui import button, card, input, select, switch, tabs
from streamlit_pages.shadcn_components import shadcn_demo, shadcn_button, shadcn_card_section, shadcn_form

def ui_components_tab():
    """
    UI Components tab showing Shadcn UI integration.
    """
    st.markdown("## Owaiken UI Components")
    st.markdown("""
    Owaiken uses modern UI components from [Shadcn UI](https://ui.shadcn.com/) to provide a beautiful and consistent user experience.
    These components are integrated using the [streamlit-shadcn-ui](https://github.com/ObservedObserver/streamlit-shadcn-ui) package.
    """)
    
    # Create tabs for different component categories
    component_tabs = st.tabs(["Overview", "Basic Components", "Form Elements", "Layout Components", "Custom Components"])
    
    with component_tabs[0]:
        st.markdown("### Overview")
        st.markdown("""
        Shadcn UI provides a set of accessible, reusable, and composable components that can be used to build modern web applications.
        These components are designed to be:
        
        - **Accessible**: All components follow WAI-ARIA guidelines
        - **Responsive**: Components adapt to different screen sizes
        - **Customizable**: Easy to customize with CSS variables
        - **Consistent**: Uniform design language across all components
        """)
        
        # Show a card with key features
        with card(title="Key Features", description="What makes Shadcn UI special"):
            st.markdown("""
            - Modern design with clean aesthetics
            - Dark and light mode support
            - Keyboard navigation support
            - Responsive and mobile-friendly
            - Seamless integration with Streamlit
            """)
            
        # Show a call-to-action
        st.markdown("### Try It Out")
        st.markdown("Explore the different component categories using the tabs above.")
        
        if shadcn_button("View All Components", variant="primary", icon="🧩"):
            st.session_state.show_all_components = True
            st.rerun()
            
        if st.session_state.get("show_all_components", False):
            shadcn_demo()
    
    with component_tabs[1]:
        st.markdown("### Basic Components")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Buttons")
            button("Default Button", variant="default")
            button("Primary Button", variant="primary")
            button("Secondary Button", variant="secondary")
            button("Destructive Button", variant="destructive")
            
            st.markdown("#### Badges")
            st.markdown("<span style='background-color: #0284c7; color: white; padding: 4px 8px; border-radius: 4px; margin-right: 5px;'>New</span>", unsafe_allow_html=True)
            st.markdown("<span style='background-color: #6b7280; color: white; padding: 4px 8px; border-radius: 4px; margin-right: 5px;'>Featured</span>", unsafe_allow_html=True)
            st.markdown("<span style='border: 1px solid #6b7280; color: #6b7280; padding: 4px 8px; border-radius: 4px; margin-right: 5px;'>Premium</span>", unsafe_allow_html=True)
            st.markdown("<span style='background-color: #ef4444; color: white; padding: 4px 8px; border-radius: 4px;'>Deprecated</span>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Alerts")
            st.info("Information alert")
            st.success("Success alert")
            st.warning("Warning alert")
            st.error("Error alert")
            
            st.markdown("#### Avatars")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div style='background-color: #0284c7; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;'>U</div>", unsafe_allow_html=True)
                st.caption("User")
            with col2:
                st.markdown("<div style='background-color: #6b7280; color: white; width: 40px; height: 40px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>A</div>", unsafe_allow_html=True)
                st.caption("Admin")
    
    with component_tabs[2]:
        st.markdown("### Form Elements")
        
        # Sample form
        st.markdown("#### Sample Form")
        form_fields = [
            {"id": "name", "label": "Full Name", "type": "input", "placeholder": "Enter your name"},
            {"id": "email", "label": "Email Address", "type": "input", "placeholder": "Enter your email", "input_type": "email"},
            {"id": "role", "label": "Role", "type": "select", "options": [
                {"label": "Developer", "value": "developer"},
                {"label": "Designer", "value": "designer"},
                {"label": "Product Manager", "value": "pm"}
            ]},
            {"id": "notifications", "label": "Enable Notifications", "type": "switch", "default": True}
        ]
        
        form_result = shadcn_form(form_fields, "Submit Form")
        
        if form_result:
            st.success("Form submitted successfully!")
            st.json(form_result)
            
        st.markdown("#### Individual Form Elements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Input Field")
            input_value = input("Username", placeholder="Enter username")
            if input_value:
                st.write(f"Input value: {input_value}")
                
            st.markdown("##### Switch")
            switch_value = switch("Dark Mode", checked=True)
            st.write(f"Switch value: {switch_value}")
        
        with col2:
            st.markdown("##### Select Dropdown")
            options = [
                {"label": "Option 1", "value": "option1"},
                {"label": "Option 2", "value": "option2"},
                {"label": "Option 3", "value": "option3"}
            ]
            selected = select("Choose an option", options=options)
            if selected:
                st.write(f"Selected: {selected}")
    
    with component_tabs[3]:
        st.markdown("### Layout Components")
        
        st.markdown("#### Cards")
        col1, col2 = st.columns(2)
        
        with col1:
            with card(title="Feature Card", description="A card showcasing a feature"):
                st.write("This card contains information about a feature.")
                button("Learn More", variant="outline")
        
        with col2:
            with card(title="Pricing Card", description="A card showing pricing information"):
                st.write("$99/month")
                st.write("All features included")
                button("Subscribe", variant="primary")
        
        st.markdown("#### Tabs")
        tab_content = tabs(
            {
                "Tab 1": "Content for Tab 1",
                "Tab 2": "Content for Tab 2",
                "Tab 3": "Content for Tab 3"
            }
        )
        st.write(f"Active tab content: {tab_content}")
    
    with component_tabs[4]:
        st.markdown("### Custom Components")
        
        st.markdown("#### Card Section")
        shadcn_card_section(
            title="Custom Card Section",
            content="This is a custom card section with actions.",
            actions=[
                {"label": "Primary Action", "variant": "primary", "on_click": lambda: None},
                {"label": "Secondary Action", "variant": "secondary", "on_click": lambda: None}
            ]
        )
        
        st.markdown("#### Enhanced Button")
        if shadcn_button("Enhanced Button with Icon", variant="primary", icon="🚀"):
            st.success("Enhanced button clicked! This button has an icon and custom click handler.")
        
        st.markdown("#### Notifications")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if button("Success Notification", variant="primary"):
                st.success("Operation completed successfully")
        
        with col2:
            if button("Error Notification", variant="destructive"):
                st.error("Something went wrong")
        
        with col3:
            if button("Info Notification", variant="secondary"):
                st.info("Just some information")
