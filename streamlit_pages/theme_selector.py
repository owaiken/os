"""
Theme selector component for Owaiken.
"""
import streamlit as st

def theme_selector():
    """
    Creates a theme selector in the sidebar that allows users to switch between light and dark themes.
    """
    with st.container():
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🌞 Light", use_container_width=True):
                st.session_state.theme = "light"
                st.experimental_set_query_params(
                    theme="light",
                    **{k: v for k, v in st.experimental_get_query_params().items() if k != "theme"}
                )
                st.rerun()
                
        with col2:
            if st.button("🌙 Dark", use_container_width=True):
                st.session_state.theme = "dark"
                st.experimental_set_query_params(
                    theme="dark", 
                    **{k: v for k, v in st.experimental_get_query_params().items() if k != "theme"}
                )
                st.rerun()
                
    # Display current theme
    current_theme = st.get_option("theme.base")
    st.caption(f"Current theme: {'Dark' if current_theme == 'dark' else 'Light'} mode")
