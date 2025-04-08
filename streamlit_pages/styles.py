"""
This module contains the CSS styles for the Streamlit UI.
"""

import streamlit as st

def load_css():
    """
    Load the custom CSS styles for the Owaiken UI with theme support.
    """
    # Force light theme for better readability
    st.markdown("""
        <style>
        /* Force light theme with good contrast */
        :root {
            --primary-color: #1E88E5;  /* Blue - more visible */
            --secondary-color: #005CB2; /* Darker Blue */
            --text-color: #000000; /* Black text for contrast */
            --background-color: #FFFFFF; /* White background */
            --logo-filter: none;
        }
        
        /* Override Streamlit's theme settings */
        .main .block-container {
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }
        
        /* Make all text black for readability */
        p, h1, h2, h3, h4, h5, h6, li, span, div {
            color: var(--text-color) !important;
        }
        
        /* Style warning messages for better visibility */
        .stAlert {
            background-color: #FFF3CD !important;
            color: #856404 !important;
            border: 1px solid #FFEEBA !important;
            border-radius: 4px !important;
            padding: 10px !important;
            margin-bottom: 16px !important;
        }
        
        .stAlert > div {
            color: #856404 !important;
        }
        
        /* Style the buttons */
        .stButton > button {
            color: black !important;
            background-color: white !important;
            border: 2px solid var(--primary-color) !important;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            color: black !important;
            border: 2px solid var(--secondary-color) !important;
            background-color: #f0f0f0 !important;
        }
        
        /* Override Streamlit's default focus styles that make buttons red */
        .stButton > button:focus, 
        .stButton > button:focus:hover, 
        .stButton > button:active, 
        .stButton > button:active:hover {
            color: black !important;
            border: 2px solid var(--secondary-color) !important;
            background-color: white !important;
            box-shadow: none !important;
            outline: none !important;
        }
        
        /* Style headers and text for light theme */
        h1, h2, h3, p, span, div, label, li {
            color: #262730 !important;
        }
        
        /* Style headers and text for dark theme */
        .dark {
            color-scheme: dark;
        }
        
        .dark h1, .dark h2, .dark h3, .dark p, .dark span, .dark div, .dark label, .dark li {
            color: white !important;
        }
        
        /* Theme toggle button styling */
        .theme-toggle {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
            background: var(--secondary-color);
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        /* Hide spans within h3 elements */
        h1 span, h2 span, h3 span {
            display: none !important;
            visibility: hidden;
            width: 0;
            height: 0;
            opacity: 0;
            position: absolute;
            overflow: hidden;
        }
        
        /* Style code blocks */
        pre {
            border-left: 4px solid var(--primary-color);
        }
        
        /* Style links */
        a {
            color: var(--secondary-color);
        }
        
        /* Style the chat messages */
        .stChatMessage {
            border-left: 4px solid var(--secondary-color);
        }
        
        /* Style the chat input */
        .stChatInput > div {
            border: 2px solid var(--primary-color) !important;
        }
        
        /* Remove red outline on focus */
        .stChatInput > div:focus-within {
            box-shadow: none !important;
            border: 2px solid var(--secondary-color) !important;
            outline: none !important;
        }
        
        /* Remove red outline on all inputs when focused */
        input:focus, textarea:focus, [contenteditable]:focus {
            box-shadow: none !important;
            border-color: var(--secondary-color) !important;
            outline: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
