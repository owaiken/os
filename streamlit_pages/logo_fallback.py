"""
Logo fallback module for Owaiken.
This module provides fallback functionality for logo display when image files are not available.
"""
import streamlit as st

def display_logo_fallback(logo_type="dark", width=250):
    """
    Display a fallback text-based logo when image files are not available.
    
    Args:
        logo_type: 'dark' or 'light' to determine the color scheme
        width: Width of the logo container
    """
    if logo_type == "dark":
        # Dark theme logo (white text)
        st.markdown(
            f"""
            <div style="width: {width}px; text-align: center; padding: 10px;">
                <h1 style="font-family: 'Arial Black', sans-serif; font-size: 32px; margin: 0; color: white;">OWAIKEN</h1>
                <p style="font-family: Arial, sans-serif; font-size: 14px; margin: 0; color: #cccccc;">AI Agent Builder</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Light theme logo (black text)
        st.markdown(
            f"""
            <div style="width: {width}px; text-align: center; padding: 10px;">
                <h1 style="font-family: 'Arial Black', sans-serif; font-size: 32px; margin: 0; color: black;">OWAIKEN</h1>
                <p style="font-family: Arial, sans-serif; font-size: 14px; margin: 0; color: #444444;">AI Agent Builder</p>
            </div>
            """,
            unsafe_allow_html=True
        )
