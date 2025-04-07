"""
Sidebar theme styling for Owaiken
Provides white sidebar for light theme and black sidebar for dark theme
"""
import streamlit as st

def apply_sidebar_theme():
    """
    Apply theme-specific styling to the sidebar
    Makes sidebar white in light theme and black in dark theme
    Also makes all input fields have white backgrounds
    And changes green text to blue
    """
    # Check current theme
    is_dark_theme = st.get_option("theme.base") == "dark"
    
    # Common CSS for both themes
    common_css = """
    /* Change any green text to blue */
    .css-1p1nwyz, .css-1p1nwyz:hover, .css-1p1nwyz:active, .css-1p1nwyz:focus,
    .css-5rimss, .css-5rimss:hover, .css-5rimss:active, .css-5rimss:focus,
    .css-1vzeuhh, .css-1vzeuhh:hover, .css-1vzeuhh:active, .css-1vzeuhh:focus,
    .css-1vbkxwb, .css-1vbkxwb:hover, .css-1vbkxwb:active, .css-1vbkxwb:focus,
    .css-1aumxhk, .css-1aumxhk:hover, .css-1aumxhk:active, .css-1aumxhk:focus,
    .css-1v0mbdj, .css-1v0mbdj:hover, .css-1v0mbdj:active, .css-1v0mbdj:focus,
    .css-1vbkxwb, .css-1vbkxwb:hover, .css-1vbkxwb:active, .css-1vbkxwb:focus,
    .css-1vzeuhh, .css-1vzeuhh:hover, .css-1vzeuhh:active, .css-1vzeuhh:focus,
    .css-5rimss, .css-5rimss:hover, .css-5rimss:active, .css-5rimss:focus,
    .css-1p1nwyz, .css-1p1nwyz:hover, .css-1p1nwyz:active, .css-1p1nwyz:focus {
        color: #3a86ff !important;
    }
    
    /* Change green backgrounds to blue */
    .css-1p1nwyz, .css-5rimss, .css-1vzeuhh, .css-1vbkxwb, .css-1aumxhk, .css-1v0mbdj,
    div[style*="background-color: rgb(10, 190, 110)"],
    div[style*="background-color: rgb(10, 190, 110, 0.1)"],
    div[style*="background-color: rgb(10, 190, 110, 0.2)"],
    div[style*="background-color: rgb(10, 190, 110, 0.3)"],
    div[style*="background-color: rgb(10, 190, 110, 0.4)"],
    div[style*="background-color: rgb(10, 190, 110, 0.5)"],
    div[style*="background-color: rgb(10, 190, 110, 0.6)"],
    div[style*="background-color: rgb(10, 190, 110, 0.7)"],
    div[style*="background-color: rgb(10, 190, 110, 0.8)"],
    div[style*="background-color: rgb(10, 190, 110, 0.9)"],
    div[style*="background-color: #0abe6e"],
    span[style*="background-color: rgb(10, 190, 110)"],
    span[style*="background-color: #0abe6e"] {
        background-color: #3a86ff !important;
    }
    
    /* Change green text to blue */
    span[style*="color: rgb(10, 190, 110)"],
    span[style*="color: #0abe6e"],
    div[style*="color: rgb(10, 190, 110)"],
    div[style*="color: #0abe6e"],
    p[style*="color: rgb(10, 190, 110)"],
    p[style*="color: #0abe6e"],
    h1[style*="color: rgb(10, 190, 110)"],
    h1[style*="color: #0abe6e"],
    h2[style*="color: rgb(10, 190, 110)"],
    h2[style*="color: #0abe6e"],
    h3[style*="color: rgb(10, 190, 110)"],
    h3[style*="color: #0abe6e"],
    h4[style*="color: rgb(10, 190, 110)"],
    h4[style*="color: #0abe6e"],
    h5[style*="color: rgb(10, 190, 110)"],
    h5[style*="color: #0abe6e"],
    h6[style*="color: rgb(10, 190, 110)"],
    h6[style*="color: #0abe6e"] {
        color: #3a86ff !important;
    }
    
    /* Change green borders to blue */
    div[style*="border-color: rgb(10, 190, 110)"],
    div[style*="border-color: #0abe6e"],
    span[style*="border-color: rgb(10, 190, 110)"],
    span[style*="border-color: #0abe6e"] {
        border-color: #3a86ff !important;
    }
    
    /* Specifically target the green API key boxes */
    .css-1p1nwyz, .css-5rimss, .css-1vzeuhh, .css-1vbkxwb {
        background-color: #3a86ff !important;
        color: white !important;
    }
    
    /* Change success messages from green to blue */
    div[data-baseweb="notification"][kind="success"] {
        background-color: #3a86ff !important;
    }
    
    /* Change info messages (often green) to blue */
    div[class*="stAlert"][kind="info"] {
        background-color: rgba(58, 134, 255, 0.2) !important;
        color: #3a86ff !important;
    }
    """
    
    if is_dark_theme:
        # Dark theme - Black sidebar with white input fields
        st.markdown(f"""
        <style>
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: #0e1117;
            color: white;
        }}
        
        /* Make all input fields white */
        .stTextInput input, 
        .stTextArea textarea, 
        .stNumberInput input,
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {{
            background-color: white !important;
            color: black !important;
        }}
        
        /* Style for select boxes */
        div[data-baseweb="select"] div {{
            background-color: white !important;
            color: black !important;
        }}
        
        /* Style for multiselect */
        div[data-baseweb="multi-select"] {{
            background-color: white !important;
        }}
        
        /* Style for date inputs */
        div[data-baseweb="datepicker"] input {{
            background-color: white !important;
            color: black !important;
        }}
        
        {common_css}
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light theme - White sidebar
        st.markdown(f"""
        <style>
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: white;
            color: black;
        }}
        
        /* Make all input fields white (already are in light theme, but ensure consistency) */
        .stTextInput input, 
        .stTextArea textarea, 
        .stNumberInput input,
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {{
            background-color: white !important;
            color: black !important;
        }}
        
        {common_css}
        </style>
        """, unsafe_allow_html=True)
