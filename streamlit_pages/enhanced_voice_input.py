"""
Enhanced Voice Input Component for Owaiken
A simplified version that uses only native Streamlit components
"""
import streamlit as st
import time
import secrets
import re
import os
import stat
from io import BytesIO
from datetime import datetime
from streamlit_pages.speech_recognition_service import transcribe_audio, sanitize_input

def create_visualizer_bars(num_bars=48, is_recording=False):
    """Create a visualization of audio bars similar to Magic UI"""
    bars_html = ""
    
    for i in range(num_bars):
        # Generate random heights when recording, fixed height when not
        if is_recording:
            height = 20 + np.random.random() * 80
            delay = i * 0.05
            bars_html += f"""
            <div 
                style="
                    width: 2px;
                    height: {height}%;
                    background-color: rgba(58, 134, 255, 0.7);
                    border-radius: 2px;
                    margin: 0 1px;
                    animation: pulse 1.5s infinite;
                    animation-delay: {delay}s;
                "
            ></div>
            """
        else:
            bars_html += f"""
            <div 
                style="
                    width: 2px;
                    height: 10%;
                    background-color: rgba(58, 134, 255, 0.3);
                    border-radius: 2px;
                    margin: 0 1px;
                "
            ></div>
            """
    
    return bars_html

def format_time(seconds):
    """Format time as MM:SS"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

# Security helper functions
def validate_key_prefix(key_prefix):
    """Validate key prefix to prevent injection attacks"""
    # Only allow alphanumeric characters and underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', key_prefix):
        # If invalid, return a safe default
        return "default"
    return key_prefix

def secure_temp_file(audio_data):
    """Create a secure temporary file for audio data"""
    if not audio_data:
        return None
        
    # Create secure temp directory if it doesn't exist
    temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)
        # Set secure permissions
        os.chmod(temp_dir, stat.S_IRWXU)  # 700 permissions
    
    # Generate secure random filename
    filename = f"audio_{secrets.token_hex(16)}.wav"
    filepath = os.path.join(temp_dir, filename)
    
    # Write data to file with secure permissions
    with open(filepath, "wb") as f:
        f.write(audio_data)
    
    # Set secure file permissions
    os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR)  # 600 permissions
    
    return filepath

def enhanced_voice_input(key_prefix="default", demo_mode=False):
    """
    Enhanced voice input component that mimics Magic UI design
    
    Args:
        key_prefix (str): Prefix for session state keys to avoid conflicts
        demo_mode (bool): If True, will work in demo mode without API keys
        
    Returns:
        str: Transcribed text if recording completed, None otherwise
    """
    # Validate key prefix for security
    key_prefix = validate_key_prefix(key_prefix)
    # Initialize session state for this component
    if f"{key_prefix}_recording" not in st.session_state:
        st.session_state[f"{key_prefix}_recording"] = False
        st.session_state[f"{key_prefix}_timer"] = 0
        st.session_state[f"{key_prefix}_audio_data"] = None
        st.session_state[f"{key_prefix}_transcription"] = None
        st.session_state[f"{key_prefix}_last_update"] = datetime.now()
    
    # CSS for animation
    st.markdown("""
    <style>
    @keyframes pulse {
        0% { opacity: 0.7; }
        50% { opacity: 1; }
        100% { opacity: 0.7; }
    }
    
    .voice-button {
        width: 64px;
        height: 64px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: none;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .voice-button:hover {
        background-color: rgba(58, 134, 255, 0.1);
    }
    
    .mic-icon {
        width: 24px;
        height: 24px;
        color: rgba(58, 134, 255, 0.7);
    }
    
    .spinner {
        width: 24px;
        height: 24px;
        border-radius: 4px;
        background-color: #3a86ff;
        animation: spin 3s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .timer {
        font-family: monospace;
        font-size: 14px;
        transition: opacity 0.3s;
    }
    
    .timer-active {
        color: rgba(58, 134, 255, 0.7);
    }
    
    .timer-inactive {
        color: rgba(58, 134, 255, 0.3);
    }
    
    .visualizer {
        height: 40px;
        width: 256px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 8px 0;
    }
    
    .status-text {
        height: 16px;
        font-size: 12px;
        color: rgba(58, 134, 255, 0.7);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create container for the component
    container = st.container()
    
    with container:
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Create the component UI
            st.markdown(f"""
            <div style="width: 100%; padding: 16px 0; display: flex; flex-direction: column; align-items: center;">
                <button 
                    class="voice-button" 
                    id="{key_prefix}_voice_button"
                    onclick="
                        window.parent.postMessage({{
                            type: 'streamlit:setComponentValue',
                            value: true,
                            dataType: 'bool',
                            key: '{key_prefix}_button_clicked'
                        }}, '*')
                    "
                >
                    {
                        '<div class="spinner"></div>' 
                        if st.session_state[f"{key_prefix}_recording"] 
                        else '<svg class="mic-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" x2="12" y1="19" y2="22"></line></svg>'
                    }
                </button>
                
                <span class="timer {
                    'timer-active' if st.session_state[f"{key_prefix}_recording"] else 'timer-inactive'
                }">
                    {format_time(st.session_state[f"{key_prefix}_timer"])}
                </span>
                
                <div class="visualizer">
                    {create_visualizer_bars(48, st.session_state[f"{key_prefix}_recording"])}
                </div>
                
                <p class="status-text">
                    {
                        "Listening..." 
                        if st.session_state[f"{key_prefix}_recording"] 
                        else "Click to speak"
                    }
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden button to handle click events from JavaScript
            if st.button("Hidden Button", key=f"{key_prefix}_button_clicked", help="", label_visibility="collapsed"):
                st.session_state[f"{key_prefix}_recording"] = not st.session_state[f"{key_prefix}_recording"]
                
                # If stopping recording, process the audio
                if not st.session_state[f"{key_prefix}_recording"]:
                    if st.session_state[f"{key_prefix}_audio_data"] is not None:
                        # Show processing message
                        with st.spinner("Processing audio..."):
                            try:
                                # Security: Create secure temp file and validate audio data
                                if st.session_state[f"{key_prefix}_audio_data"] and len(st.session_state[f"{key_prefix}_audio_data"]) < 10 * 1024 * 1024:  # 10MB limit
                                    # Transcribe the audio
                                    transcription = transcribe_audio(st.session_state[f"{key_prefix}_audio_data"])
                                    
                                    # Check if there was an error with the API key
                                    if transcription and isinstance(transcription, str) and transcription.startswith("Error:"):
                                        if demo_mode:
                                            # In demo mode, return a placeholder response
                                            transcription = "This is a demo transcription. Please configure your API key for actual transcription."
                                        else:
                                            # Show generic error message (don't expose specific API details)
                                            st.error("Speech recognition service unavailable. Please contact your administrator.")
                                            transcription = None
                                    
                                    # Sanitize the transcription before storing it
                                    if transcription:
                                        transcription = sanitize_input(transcription)
                                        
                                    st.session_state[f"{key_prefix}_transcription"] = transcription
                                else:
                                    # Invalid or oversized audio data
                                    st.error("Invalid audio data or file size too large")
                                    transcription = None
                            except Exception as e:
                                # Log error type but not details (could contain sensitive info)
                                error_type = type(e).__name__
                                print(f"Voice processing error: {error_type}")
                                st.error("An error occurred while processing your audio")
                                
                                if demo_mode:
                                    # In demo mode, return a placeholder response
                                    st.session_state[f"{key_prefix}_transcription"] = "This is a demo transcription. Please configure your API key for actual transcription."
                    
                    # Reset timer and audio data
                    st.session_state[f"{key_prefix}_timer"] = 0
                    st.session_state[f"{key_prefix}_audio_data"] = None
    
    # Handle recording state
    if st.session_state[f"{key_prefix}_recording"]:
        # Record audio
        audio_data = st.audio_recorder(
            pause_threshold=60.0,
            sample_rate=16000,
            key=f"{key_prefix}_recorder"
        )
        
        if audio_data is not None:
            st.session_state[f"{key_prefix}_audio_data"] = audio_data
        
        # Update timer
        now = datetime.now()
        if (now - st.session_state[f"{key_prefix}_last_update"]).total_seconds() >= 1:
            st.session_state[f"{key_prefix}_timer"] += 1
            st.session_state[f"{key_prefix}_last_update"] = now
            st.rerun()
    
    # Return transcription if available
    transcription = st.session_state.get(f"{key_prefix}_transcription")
    if transcription:
        # Clear the transcription for next use
        st.session_state[f"{key_prefix}_transcription"] = None
        return transcription
    
    return None
