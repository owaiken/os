"""
Dark UI theme and components for OpenManus integration
"""
import streamlit as st

def apply_dark_theme():
    """
    Apply dark theme styling for OpenManus interface
    """
    st.markdown("""
    <style>
    /* Dark theme for OpenManus */
    .openmanus-container {
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 20px;
        color: white;
        margin-bottom: 20px;
    }
    
    .openmanus-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }
    
    .openmanus-title {
        font-size: 24px;
        font-weight: bold;
        color: #3a86ff;
    }
    
    .openmanus-beta {
        background-color: #3a86ff;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        margin-left: 10px;
    }
    
    .openmanus-computer {
        background-color: #0f0f0f;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
    }
    
    .openmanus-computer-image {
        width: 100px;
        margin: 0 auto;
        display: block;
    }
    
    .openmanus-status {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
        font-size: 14px;
    }
    
    .openmanus-status-dot {
        width: 10px;
        height: 10px;
        background-color: #3a86ff;
        border-radius: 50%;
        margin-right: 10px;
    }
    
    .openmanus-task-input {
        background-color: #2a2a2a;
        border: none;
        border-radius: 5px;
        padding: 15px;
        color: white;
        width: 100%;
        margin-top: 20px;
    }
    
    .openmanus-button {
        background-color: #3a86ff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .openmanus-button:hover {
        background-color: #2a75e8;
    }
    
    .openmanus-instructions {
        background-color: #2a2a2a;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    
    .openmanus-instructions h3 {
        color: #3a86ff;
        margin-bottom: 15px;
    }
    
    .openmanus-instructions ol {
        margin-left: 20px;
        padding-left: 0;
    }
    
    .openmanus-instructions li {
        margin-bottom: 10px;
    }
    
    .openmanus-voice-button {
        background-color: #2a2a2a;
        border: 1px solid #3a86ff;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .openmanus-voice-button:hover {
        background-color: #3a3a3a;
    }
    
    .openmanus-voice-button.recording {
        background-color: #ff3a3a;
        border-color: #ff3a3a;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
        100% {
            transform: scale(1);
        }
    }
    
    .openmanus-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
        border-top: 1px solid #333;
        padding-top: 10px;
        font-size: 12px;
        color: #888;
    }
    
    /* Task history styling */
    .task-history {
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .task-history-header {
        color: #3a86ff;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .task-history-item {
        background-color: #2a2a2a;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Computer display styling */
    .computer-display {
        background-color: #0f0f0f;
        border: 2px solid #333;
        border-radius: 10px;
        padding: 20px;
        height: 400px;
        overflow-y: auto;
        font-family: monospace;
        color: #3a86ff;
    }
    
    .computer-display-header {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    
    .computer-display-content {
        white-space: pre-wrap;
    }
    
    /* Button styling */
    .action-button {
        background-color: #2a2a2a;
        border: 1px solid #3a86ff;
        color: #3a86ff;
        border-radius: 5px;
        padding: 5px 10px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .action-button:hover {
        background-color: #3a3a3a;
    }
    
    /* Voice recording animation */
    .voice-waves {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 30px;
    }
    
    .voice-wave {
        width: 3px;
        height: 15px;
        margin: 0 2px;
        background-color: #3a86ff;
        animation: wave 1s infinite ease-in-out;
    }
    
    .voice-wave:nth-child(2) {
        animation-delay: 0.1s;
    }
    
    .voice-wave:nth-child(3) {
        animation-delay: 0.2s;
    }
    
    .voice-wave:nth-child(4) {
        animation-delay: 0.3s;
    }
    
    .voice-wave:nth-child(5) {
        animation-delay: 0.4s;
    }
    
    @keyframes wave {
        0%, 100% {
            height: 5px;
        }
        50% {
            height: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def computer_svg():
    """
    Return SVG for computer icon
    """
    return """
    <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="10" width="80" height="60" rx="5" fill="#333" stroke="#3a86ff" stroke-width="2"/>
        <rect x="15" y="15" width="70" height="50" rx="2" fill="#111"/>
        <rect x="35" y="70" width="30" height="10" fill="#333"/>
        <rect x="25" y="80" width="50" height="5" rx="2" fill="#333"/>
    </svg>
    """

def microphone_svg(recording=False):
    """
    Return SVG for microphone icon
    """
    color = "#ff3a3a" if recording else "#3a86ff"
    return f"""
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="{color}"/>
        <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="{color}"/>
    </svg>
    """

def reconnect_svg():
    """
    Return SVG for reconnect icon
    """
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z" fill="#3a86ff"/>
    </svg>
    """

def fullscreen_svg():
    """
    Return SVG for fullscreen icon
    """
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z" fill="#3a86ff"/>
    </svg>
    """
