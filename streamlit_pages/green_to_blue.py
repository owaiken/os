"""
Direct CSS to change green text to blue
"""
import streamlit as st

def change_green_to_blue():
    """
    Apply direct CSS to change green text to blue
    """
    st.markdown("""
    <style>
    /* Target the specific green elements in the Environment Configuration */
    .element-container:has(span:contains("API_URL")) span,
    .element-container:has(span:contains("API_KEY")) span,
    .element-container:has(span:contains("PLANNER_URL")) span,
    .element-container:has(span:contains("SUPABASE_URL")) span,
    .element-container:has(span:contains("SUPABASE_API_KEY")) span,
    .element-container:has(span:contains("AGENT_MODEL")) span,
    .element-container:has(span:contains("PLANNER_MODEL")) span {
        background-color: #3a86ff !important;
        color: white !important;
    }
    
    /* Target all elements with inline style for green background */
    [style*="background-color: rgb(10, 190, 110)"] {
        background-color: #3a86ff !important;
    }
    
    /* Target all elements with inline style for green text */
    [style*="color: rgb(10, 190, 110)"] {
        color: #3a86ff !important;
    }
    
    /* Target specific green elements by their content */
    span:contains("API_URL"),
    span:contains("API_KEY"),
    span:contains("PLANNER_URL"),
    span:contains("SUPABASE_URL"),
    span:contains("SUPABASE_API_KEY"),
    span:contains("AGENT_MODEL"),
    span:contains("PLANNER_MODEL") {
        background-color: #3a86ff !important;
        color: white !important;
    }
    
    /* Force override any green backgrounds */
    .stAlert {
        background-color: rgba(58, 134, 255, 0.2) !important;
    }
    
    /* Target the specific green elements by their exact CSS class */
    .css-nahz7x, /* This is a common class for green elements */
    .css-1p1nwyz,
    .css-5rimss,
    .css-1vzeuhh,
    .css-1vbkxwb,
    .css-1aumxhk,
    .css-1v0mbdj {
        background-color: #3a86ff !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
