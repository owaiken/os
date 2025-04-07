"""
Custom theme styling for Owaiken
Provides dark and light theme options with GlobalGPT-inspired styling
"""
import streamlit as st

def apply_custom_theme(theme="dark"):
    """
    Apply custom theme styling to the Streamlit app
    
    Args:
        theme: "dark" or "light"
    """
    if theme == "dark":
        # Dark theme styling
        st.markdown("""
        <style>
        /* Main background and text colors */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #1a1c24;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Sidebar navigation items */
        .css-1d391kg, .css-1lsmgbg {
            background-color: #1a1c24 !important;
        }
        
        div[data-testid="stSidebarNav"] > ul {
            padding-top: 2rem;
            padding-left: 0.5rem;
        }
        
        div[data-testid="stSidebarNav"] li {
            margin-bottom: 0.5rem;
        }
        
        div[data-testid="stSidebarNav"] a {
            border-radius: 0.5rem;
            padding: 0.5rem 0.8rem;
            text-decoration: none;
            font-size: 1rem;
            display: flex;
            align-items: center;
            color: rgba(250, 250, 250, 0.8);
            font-weight: 400;
            transition: all 0.2s ease;
        }
        
        div[data-testid="stSidebarNav"] a:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
        }
        
        div[data-testid="stSidebarNav"] a.active {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            font-weight: 600;
        }
        
        /* Sidebar logo area */
        div[data-testid="stSidebarNav"] > div:first-child {
            padding: 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 0.5rem;
        }
        
        /* Custom logo styling */
        .sidebar-logo {
            display: flex;
            align-items: center;
            padding: 1rem 1rem 2rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .sidebar-logo img {
            width: 40px;
            height: 40px;
            margin-right: 10px;
        }
        
        .sidebar-logo-text {
            font-size: 1.5rem;
            font-weight: 600;
            color: white;
        }
        
        /* Buttons */
        .stButton button {
            background-color: #3a86ff;
            color: white;
            border-radius: 0.5rem;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            background-color: #2a76ef;
            color: white;
        }
        
        /* Input fields */
        .stTextInput input, .stTextArea textarea {
            background-color: #1a1c24;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
            color: white;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 2.5rem;
            white-space: pre-wrap;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 0.5rem;
            color: rgba(250, 250, 250, 0.8);
            padding: 0.5rem 1rem;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #3a86ff !important;
            color: white !important;
        }
        
        /* Cards and containers */
        [data-testid="stExpander"] {
            background-color: #1a1c24;
            border-radius: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Custom sidebar section */
        .sidebar-section {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0.5rem;
        }
        
        .sidebar-section-title {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: rgba(250, 250, 250, 0.8);
        }
        
        /* Custom sidebar items */
        .sidebar-item {
            display: flex;
            align-items: center;
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .sidebar-item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        .sidebar-item-icon {
            margin-right: 0.5rem;
            width: 1.5rem;
            text-align: center;
        }
        
        .sidebar-item-text {
            font-size: 0.9rem;
            color: rgba(250, 250, 250, 0.8);
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light theme styling
        st.markdown("""
        <style>
        /* Main background and text colors */
        .stApp {
            background-color: #ffffff;
            color: #111111;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #f5f5f5;
            border-right: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        /* Sidebar navigation items */
        .css-1d391kg, .css-1lsmgbg {
            background-color: #f5f5f5 !important;
        }
        
        div[data-testid="stSidebarNav"] > ul {
            padding-top: 2rem;
            padding-left: 0.5rem;
        }
        
        div[data-testid="stSidebarNav"] li {
            margin-bottom: 0.5rem;
        }
        
        div[data-testid="stSidebarNav"] a {
            border-radius: 0.5rem;
            padding: 0.5rem 0.8rem;
            text-decoration: none;
            font-size: 1rem;
            display: flex;
            align-items: center;
            color: rgba(0, 0, 0, 0.8);
            font-weight: 400;
            transition: all 0.2s ease;
        }
        
        div[data-testid="stSidebarNav"] a:hover {
            background-color: rgba(0, 0, 0, 0.05);
            color: #000000;
        }
        
        div[data-testid="stSidebarNav"] a.active {
            background-color: rgba(0, 0, 0, 0.05);
            color: #000000;
            font-weight: 600;
        }
        
        /* Sidebar logo area */
        div[data-testid="stSidebarNav"] > div:first-child {
            padding: 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 0.5rem;
        }
        
        /* Custom logo styling */
        .sidebar-logo {
            display: flex;
            align-items: center;
            padding: 1rem 1rem 2rem 1rem;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        .sidebar-logo img {
            width: 40px;
            height: 40px;
            margin-right: 10px;
        }
        
        .sidebar-logo-text {
            font-size: 1.5rem;
            font-weight: 600;
            color: #000000;
        }
        
        /* Buttons */
        .stButton button {
            background-color: #3a86ff;
            color: white;
            border-radius: 0.5rem;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            background-color: #2a76ef;
            color: white;
        }
        
        /* Input fields */
        .stTextInput input, .stTextArea textarea {
            background-color: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 0.5rem;
            color: #000000;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 2.5rem;
            white-space: pre-wrap;
            background-color: rgba(0, 0, 0, 0.05);
            border-radius: 0.5rem;
            color: rgba(0, 0, 0, 0.8);
            padding: 0.5rem 1rem;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #3a86ff !important;
            color: white !important;
        }
        
        /* Cards and containers */
        [data-testid="stExpander"] {
            background-color: #ffffff;
            border-radius: 0.5rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        /* Custom sidebar section */
        .sidebar-section {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0.5rem;
        }
        
        .sidebar-section-title {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: rgba(0, 0, 0, 0.8);
        }
        
        /* Custom sidebar items */
        .sidebar-item {
            display: flex;
            align-items: center;
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .sidebar-item:hover {
            background-color: rgba(0, 0, 0, 0.05);
        }
        
        .sidebar-item-icon {
            margin-right: 0.5rem;
            width: 1.5rem;
            text-align: center;
        }
        
        .sidebar-item-text {
            font-size: 0.9rem;
            color: rgba(0, 0, 0, 0.8);
        }
        </style>
        """, unsafe_allow_html=True)

def create_sidebar_logo():
    """
    Create a custom logo in the sidebar similar to GlobalGPT
    """
    st.markdown("""
    <div class="sidebar-logo">
        <div style="width: 40px; height: 40px; background: linear-gradient(45deg, #ff5e62, #ff9966); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 20px; font-weight: bold;">O</span>
        </div>
        <div class="sidebar-logo-text">Owaiken</div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar_item(icon, text, key=None):
    """
    Create a custom sidebar item with icon and text
    
    Args:
        icon: Icon emoji or HTML
        text: Item text
        key: Optional key for button
    
    Returns:
        True if item is clicked, False otherwise
    """
    clicked = False
    html = f"""
    <div class="sidebar-item" id="{key or text.lower().replace(' ', '-')}">
        <div class="sidebar-item-icon">{icon}</div>
        <div class="sidebar-item-text">{text}</div>
    </div>
    """
    
    if key:
        clicked = st.button(text, key=key, help=text)
    else:
        st.markdown(html, unsafe_allow_html=True)
    
    return clicked

def create_sidebar_section(title, items):
    """
    Create a custom sidebar section with title and items
    
    Args:
        title: Section title
        items: List of (icon, text) tuples
    """
    st.markdown(f"""
    <div class="sidebar-section">
        <div class="sidebar-section-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)
    
    for icon, text in items:
        create_sidebar_item(icon, text)
