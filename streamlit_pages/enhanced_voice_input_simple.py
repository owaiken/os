"""
Simplified Enhanced Voice Input Component for Owaiken
Uses only native Streamlit components for better compatibility
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

def format_time(seconds):
    """Format time as MM:SS"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

def simplified_voice_input(key_prefix="default", demo_mode=False):
    """
    Simplified voice input component using native Streamlit elements
    
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
    
    # Create container for the component
    container = st.container()
    
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Display recording status
            if st.session_state[f"{key_prefix}_recording"]:
                status_text = "Recording in progress..."
                progress_value = 100
                # Update timer
                current_time = datetime.now()
                time_diff = (current_time - st.session_state[f"{key_prefix}_last_update"]).total_seconds()
                st.session_state[f"{key_prefix}_timer"] += time_diff
                st.session_state[f"{key_prefix}_last_update"] = current_time
            else:
                status_text = "Click to start recording"
                progress_value = 0
            
            # Display timer
            if st.session_state[f"{key_prefix}_timer"] > 0:
                st.text(f"Recording time: {format_time(int(st.session_state[f'{key_prefix}_timer']))}")
            
            # Display progress bar as a visual indicator
            st.progress(progress_value, text=status_text)
            
            # Record/Stop button
            button_text = "Stop Recording" if st.session_state[f"{key_prefix}_recording"] else "Start Recording"
            button_color = "danger" if st.session_state[f"{key_prefix}_recording"] else "primary"
            
            if st.button(button_text, key=f"{key_prefix}_record_button", type=button_color):
                if st.session_state[f"{key_prefix}_recording"]:
                    # Stop recording
                    st.session_state[f"{key_prefix}_recording"] = False
                    
                    # In a real implementation, we would process the audio data here
                    # For demo purposes, we'll simulate a successful recording
                    if demo_mode:
                        st.session_state[f"{key_prefix}_transcription"] = "This is a demo transcription. The actual transcription would appear here."
                    else:
                        # Process the audio data (simulated for now)
                        st.info("Processing audio...")
                        time.sleep(1)  # Simulate processing time
                        st.session_state[f"{key_prefix}_transcription"] = "Sample transcription from audio recording."
                    
                    # Reset timer
                    st.session_state[f"{key_prefix}_timer"] = 0
                    st.rerun()
                else:
                    # Start recording
                    st.session_state[f"{key_prefix}_recording"] = True
                    st.session_state[f"{key_prefix}_last_update"] = datetime.now()
                    st.session_state[f"{key_prefix}_transcription"] = None
                    st.rerun()
            
            # Display transcription if available
            if st.session_state[f"{key_prefix}_transcription"]:
                st.text_area("Transcription", st.session_state[f"{key_prefix}_transcription"], 
                             height=100, key=f"{key_prefix}_transcription_area")
    
    # Return the transcription if available
    return st.session_state.get(f"{key_prefix}_transcription")
