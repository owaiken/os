"""
Cloud-Safe Voice Input Component for Owaiken
A minimal implementation that works reliably in cloud environments
"""
import streamlit as st
import time
import secrets
import re
import os
import stat
from datetime import datetime
from streamlit_pages.speech_recognition_service import transcribe_audio, sanitize_input

def cloud_safe_voice_input(key_prefix="default", demo_mode=False):
    """
    Cloud-safe voice input component that works reliably in cloud environments
    
    Args:
        key_prefix (str): Prefix for session state keys to avoid conflicts
        demo_mode (bool): If True, will work in demo mode without API keys
        
    Returns:
        str: Transcribed text if recording completed, None otherwise
    """
    # Initialize session state
    if f"{key_prefix}_transcription" not in st.session_state:
        st.session_state[f"{key_prefix}_transcription"] = None
    
    # Simple container with file uploader and demo option
    st.write("### Voice Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # File uploader for audio
        uploaded_file = st.file_uploader("Upload audio file (WAV, MP3, M4A)", 
                                         type=["wav", "mp3", "m4a"], 
                                         key=f"{key_prefix}_file_uploader")
        
        if uploaded_file is not None:
            # Process the uploaded audio file
            if demo_mode:
                # Demo mode - simulate transcription
                with st.spinner("Transcribing audio..."):
                    time.sleep(2)  # Simulate processing time
                    st.session_state[f"{key_prefix}_transcription"] = "This is a demo transcription from the uploaded audio file."
                    st.success("Audio transcribed successfully!")
            else:
                # Real transcription using the speech recognition service
                try:
                    with st.spinner("Transcribing audio..."):
                        audio_bytes = uploaded_file.getvalue()
                        transcription = transcribe_audio(audio_bytes)
                        if transcription:
                            # Sanitize the input for security
                            transcription = sanitize_input(transcription)
                            st.session_state[f"{key_prefix}_transcription"] = transcription
                            st.success("Audio transcribed successfully!")
                        else:
                            st.error("Failed to transcribe audio. Please try again.")
                except Exception as e:
                    st.error(f"Error transcribing audio: {str(e)}")
    
    with col2:
        # Demo button for quick testing
        if demo_mode and st.button("Generate Demo Transcription", key=f"{key_prefix}_demo_button"):
            with st.spinner("Generating demo transcription..."):
                time.sleep(1)  # Simulate processing time
                demo_texts = [
                    "Create a simple weather app using Python and OpenWeatherMap API.",
                    "Build a task management system with priority levels and due dates.",
                    "Develop a data visualization dashboard for sales analytics.",
                    "Write a script to automate file organization based on file types."
                ]
                import random
                st.session_state[f"{key_prefix}_transcription"] = random.choice(demo_texts)
                st.success("Demo transcription generated!")
    
    # Display the transcription if available
    if st.session_state.get(f"{key_prefix}_transcription"):
        st.text_area("Transcription", st.session_state[f"{key_prefix}_transcription"], 
                     height=100, key=f"{key_prefix}_transcription_area")
        
        # Clear button
        if st.button("Clear Transcription", key=f"{key_prefix}_clear_button"):
            st.session_state[f"{key_prefix}_transcription"] = None
            st.experimental_rerun()
    
    # Return the transcription
    return st.session_state.get(f"{key_prefix}_transcription")
