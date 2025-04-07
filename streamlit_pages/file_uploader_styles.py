"""
Custom styles for file uploader components in Owaiken.
"""
import streamlit as st

def apply_file_uploader_styles():
    """
    Apply custom styles to file uploader components to give them a glass/blur effect with white background.
    """
    st.markdown("""
    <style>
    /* File uploader styling with glass effect */
    [data-testid="stFileUploaderDropzone"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Hover effect */
    [data-testid="stFileUploaderDropzone"]:hover {
        background-color: rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Button inside file uploader */
    [data-testid="stFileUploaderDropzone"] button {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
        border-radius: 4px !important;
        padding: 0.3rem 1rem !important;
        font-weight: normal !important;
    }
    
    /* Text inside file uploader */
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] small {
        color: black !important;
    }
    
    /* Icon inside file uploader */
    [data-testid="stFileUploaderDropzone"] svg {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)
