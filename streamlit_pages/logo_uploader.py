"""
Logo uploader module for Owaiken.
This module provides functionality for uploading and saving logo files.
"""
import streamlit as st
import os
import base64
from streamlit_pages.file_uploader_styles import apply_file_uploader_styles

def logo_uploader_tab():
    """
    Tab for uploading and managing logo files.
    """
    # Apply custom styles to file uploaders
    apply_file_uploader_styles()
    
    st.markdown("## Logo Management")
    st.markdown("Upload your logo files for the application. The logos will be saved to the public directory.")
    
    # Create columns for light and dark logos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Light Theme Logo (Black)")
        light_logo = st.file_uploader("Upload black logo for light theme", type=["svg", "png"], key="light_logo")
        
        if light_logo is not None:
            # Display the uploaded logo
            file_details = {"Filename": light_logo.name, "FileType": light_logo.type, "Size": light_logo.size}
            st.write(file_details)
            
            # Display preview
            if light_logo.type.startswith("image"):
                st.image(light_logo, width=200)
            
            # Save button
            if st.button("Save Light Theme Logo"):
                file_path = save_logo(light_logo, "Owaiken_Black")
                st.success(f"✅ Saved as {file_path}")
                
                # Display a message about restarting the app
                st.info("The logo has been saved. Please refresh the page to see the changes.")
                
                # Add a restart button
                if st.button("Refresh Application", key="refresh_light"):
                    st.rerun()
    
    with col2:
        st.markdown("### Dark Theme Logo (White)")
        dark_logo = st.file_uploader("Upload white logo for dark theme", type=["svg", "png"], key="dark_logo")
        
        if dark_logo is not None:
            # Display the uploaded logo
            file_details = {"Filename": dark_logo.name, "FileType": dark_logo.type, "Size": dark_logo.size}
            st.write(file_details)
            
            # Display preview
            if dark_logo.type.startswith("image"):
                st.image(dark_logo, width=200)
            
            # Save button
            if st.button("Save Dark Theme Logo"):
                file_path = save_logo(dark_logo, "Owaiken_White")
                st.success(f"✅ Saved as {file_path}")
                
                # Display a message about restarting the app
                st.info("The logo has been saved. Please refresh the page to see the changes.")
                
                # Add a restart button
                if st.button("Refresh Application", key="refresh_dark"):
                    st.rerun()
    
    # Display current logos
    st.markdown("### Current Logos")
    
    current_col1, current_col2 = st.columns(2)
    
    with current_col1:
        st.markdown("#### Light Theme Logo")
        light_logo_path = find_logo("Owaiken_Black")
        if light_logo_path and os.path.getsize(light_logo_path) > 10:  # Make sure file is not empty
            try:
                st.image(light_logo_path, width=200)
                st.success("✅ Light theme logo is set up correctly")
                st.caption(f"Path: {light_logo_path}")
            except Exception as e:
                st.error(f"Error displaying logo: {str(e)}")
        else:
            st.warning("No valid light theme logo found. Please upload one.")
    
    with current_col2:
        st.markdown("#### Dark Theme Logo")
        dark_logo_path = find_logo("Owaiken_White")
        if dark_logo_path and os.path.getsize(dark_logo_path) > 10:  # Make sure file is not empty
            try:
                st.image(dark_logo_path, width=200)
                st.success("✅ Dark theme logo is set up correctly")
                st.caption(f"Path: {dark_logo_path}")
            except Exception as e:
                st.error(f"Error displaying logo: {str(e)}")
        else:
            st.warning("No valid dark theme logo found. Please upload one.")
            
    # Add a manual refresh button
    if st.button("Refresh Display", key="refresh_display"):
        st.rerun()
    
    # SVG direct input
    st.markdown("### Direct SVG Input")
    st.markdown("If you have an SVG file, you can paste its content directly here:")
    
    svg_content = st.text_area("SVG Content", height=200, placeholder='<svg xmlns="http://www.w3.org/2000/svg">...</svg>')
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Save as Light Theme Logo") and svg_content:
            file_path = save_svg_content(svg_content, "Owaiken_Black.svg")
            st.success(f"✅ Saved as {file_path}")
            
            # Display a message about restarting the app
            st.info("The logo has been saved. Please refresh the page to see the changes.")
            
            # Add a restart button
            if st.button("Refresh Application", key="refresh_svg_light"):
                st.rerun()
    
    with col2:
        if st.button("Save as Dark Theme Logo") and svg_content:
            file_path = save_svg_content(svg_content, "Owaiken_White.svg")
            st.success(f"✅ Saved as {file_path}")
            
            # Display a message about restarting the app
            st.info("The logo has been saved. Please refresh the page to see the changes.")
            
            # Add a restart button
            if st.button("Refresh Application", key="refresh_svg_dark"):
                st.rerun()

def save_logo(uploaded_file, base_name):
    """
    Save an uploaded logo file to the public directory.
    
    Args:
        uploaded_file: The uploaded file object
        base_name: Base name for the saved file (without extension)
    """
    # Get the current directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create public directory if it doesn't exist
    public_dir = os.path.join(current_dir, "public")
    os.makedirs(public_dir, exist_ok=True)
    
    # Get file extension
    file_extension = uploaded_file.name.split(".")[-1]
    
    # Save the file
    file_path = os.path.join(public_dir, f"{base_name}.{file_extension}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return file_path

def save_svg_content(svg_content, filename):
    """
    Save SVG content to a file.
    
    Args:
        svg_content: The SVG content as a string
        filename: The filename to save as
    """
    # Get the current directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create public directory if it doesn't exist
    public_dir = os.path.join(current_dir, "public")
    os.makedirs(public_dir, exist_ok=True)
    
    # Save the SVG content
    file_path = os.path.join(public_dir, filename)
    with open(file_path, "w") as f:
        f.write(svg_content)
        
    return file_path

def find_logo(base_name):
    """
    Find a logo file in the public directory.
    
    Args:
        base_name: Base name of the logo file (without extension)
    
    Returns:
        Path to the logo file if found, None otherwise
    """
    # Get the current directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_dir = os.path.join(current_dir, "public")
    
    # Check for SVG
    svg_path = os.path.join(public_dir, f"{base_name}.svg")
    if os.path.exists(svg_path):
        return svg_path
    
    # Check for PNG
    png_path = os.path.join(public_dir, f"{base_name}.png")
    if os.path.exists(png_path):
        return png_path
    
    # Check for other common image formats
    for ext in ["jpg", "jpeg", "gif"]:
        path = os.path.join(public_dir, f"{base_name}.{ext}")
        if os.path.exists(path):
            return path
    
    return None

def get_svg_as_base64(svg_path):
    """
    Read an SVG file and return its content as a base64 encoded string.
    
    Args:
        svg_path: Path to the SVG file
    
    Returns:
        Base64 encoded SVG content
    """
    try:
        with open(svg_path, "r") as f:
            svg_content = f.read()
        return base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
    except:
        return None
