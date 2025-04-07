"""
Logo handler module for Owaiken.
This module provides functionality for displaying logos in the application.
"""
import streamlit as st
import base64
from pathlib import Path

# Logo data will be embedded directly in the code
# This ensures the logos are always available regardless of file system issues

# Base64 encoded logo data would normally go here
# For now, we'll use a simplified version that creates SVG logos directly

def get_logo_svg(logo_type="dark"):
    """
    Generate an SVG logo based on the provided logo type.
    
    Args:
        logo_type: 'dark' for white logo (dark theme) or 'light' for black logo (light theme)
    
    Returns:
        SVG string of the logo
    """
    # Set color based on theme
    color = "white" if logo_type == "dark" else "black"
    
    # Create an accurate SVG representation of the Owaiken logo
    svg = f"""
    <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <g fill="{color}">
            <!-- Outer circle -->
            <path d="M100,0C44.8,0,0,44.8,0,100s44.8,100,100,100s100-44.8,100-100S155.2,0,100,0z M100,180c-44.1,0-80-35.9-80-80
                s35.9-80,80-80s80,35.9,80,80S144.1,180,100,180z"/>
            
            <!-- Top arc -->
            <path d="M160,60c-16.4-16.4-38.8-26.7-63.5-26.7c-24.7,0-47.1,10.3-63.5,26.7l14.1,14.1c13.1-13.1,31-21.2,50.8-21.2
                s37.7,8.1,50.8,21.2L160,60z"/>
            
            <!-- Middle horizontal line -->
            <rect x="30" y="90" width="140" height="20"/>
            
            <!-- Bottom arc -->
            <path d="M160,140c-16.4,16.4-38.8,26.7-63.5,26.7c-24.7,0-47.1-10.3-63.5-26.7l14.1-14.1c13.1,13.1,31,21.2,50.8,21.2
                s37.7-8.1,50.8-21.2L160,140z"/>
        </g>
    </svg>
    """
    
    return svg

def display_logo(logo_type="dark", width=250):
    """
    Display the Owaiken logo.
    
    Args:
        logo_type: 'dark' for white logo (dark theme) or 'light' for black logo (light theme)
        width: Width of the logo in pixels
    """
    svg = get_logo_svg(logo_type)
    
    # Convert SVG to base64 for embedding in HTML
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    
    # Display the logo using HTML
    html = f"""
    <div style="width: {width}px; text-align: center;">
        <img src="data:image/svg+xml;base64,{b64}" width="{width}" />
        <p style="font-family: Arial, sans-serif; font-size: 14px; margin: 0; color: {'#cccccc' if logo_type == 'dark' else '#444444'};">AI Agent Builder</p>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
