"""
Direct CSS override to change green elements to blue
"""
import streamlit as st

def apply_direct_css_override():
    """
    Apply direct CSS to override green elements with blue
    Uses very specific selectors to target the environment configuration elements
    """
    st.markdown("""
    <style>
    /* Direct override for green API key boxes */
    .st-emotion-cache-nahz7x,
    .st-emotion-cache-5rimss,
    .st-emotion-cache-1vzeuhh,
    .st-emotion-cache-1vbkxwb,
    .st-emotion-cache-1aumxhk,
    .st-emotion-cache-1v0mbdj,
    .st-emotion-cache-1p1nwyz {
        background-color: #3a86ff !important;
        color: white !important;
    }
    
    /* Target any element with green background */
    div[style*="background-color: rgb(10, 190, 110)"],
    span[style*="background-color: rgb(10, 190, 110)"],
    div[style*="background-color: #0abe6e"],
    span[style*="background-color: #0abe6e"] {
        background-color: #3a86ff !important;
    }
    
    /* Target any element with green text */
    div[style*="color: rgb(10, 190, 110)"],
    span[style*="color: rgb(10, 190, 110)"],
    div[style*="color: #0abe6e"],
    span[style*="color: #0abe6e"] {
        color: #3a86ff !important;
    }
    
    /* Target success messages */
    .stAlert[kind="success"] {
        background-color: rgba(58, 134, 255, 0.2) !important;
        color: #3a86ff !important;
    }
    
    /* Target info messages */
    .stAlert[kind="info"] {
        background-color: rgba(58, 134, 255, 0.2) !important;
        color: #3a86ff !important;
    }
    
    /* Target the specific green elements in the Environment tab */
    [data-testid="stExpander"] .element-container:nth-child(n) span[style*="background-color: rgb(10, 190, 110)"],
    [data-testid="stExpander"] .element-container:nth-child(n) span[style*="background-color: #0abe6e"] {
        background-color: #3a86ff !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
