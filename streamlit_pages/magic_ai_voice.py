"""
Magic Design AI Voice Input Component for Streamlit
"""
import streamlit as st
from datetime import datetime
import time
import base64
import json
import os
from streamlit_pages.speech_recognition_service import get_speech_recognition_service

def apply_magic_voice_styles():
    """
    Apply Magic Design styling for the AI Voice Input component
    """
    st.markdown("""
    <style>
    /* Magic Design Voice Input Component */
    .magic-voice-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 20px 0;
    }
    
    .magic-voice-button {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #2a2a2a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .magic-voice-button:hover {
        transform: scale(1.05);
        background-color: #333;
    }
    
    .magic-voice-button.recording {
        background-color: #ff3a3a;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 58, 58, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(255, 58, 58, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 58, 58, 0);
        }
    }
    
    .magic-voice-status {
        margin-top: 10px;
        font-size: 14px;
        color: #888;
    }
    
    .magic-voice-status.recording {
        color: #ff3a3a;
    }
    
    .magic-voice-visualization {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 40px;
        margin-top: 10px;
    }
    
    .magic-voice-bar {
        width: 3px;
        height: 20px;
        margin: 0 2px;
        background-color: #3a86ff;
        border-radius: 3px;
        animation: sound-wave 0.5s infinite alternate;
    }
    
    @keyframes sound-wave {
        0% {
            height: 5px;
        }
        100% {
            height: 30px;
        }
    }
    
    .magic-voice-bar:nth-child(1) { animation-delay: 0.0s; }
    .magic-voice-bar:nth-child(2) { animation-delay: 0.1s; }
    .magic-voice-bar:nth-child(3) { animation-delay: 0.2s; }
    .magic-voice-bar:nth-child(4) { animation-delay: 0.3s; }
    .magic-voice-bar:nth-child(5) { animation-delay: 0.4s; }
    
    .magic-voice-recordings {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 16px;
        width: 100%;
        max-width: 300px;
    }
    
    .magic-voice-recording {
        background-color: #2a2a2a;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 12px;
        color: #fff;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .magic-voice-recording-info {
        display: flex;
        flex-direction: column;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add JavaScript for audio recording
    audio_recorder_js = """
    <script>
    // Create a self-executing function to avoid global namespace pollution
    (function() {
        // Check if browser supports audio recording
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            console.log('Audio recording is supported in this browser');
        } else {
            console.error('Audio recording is not supported in this browser');
        }
        
        // Variables for recording
        let mediaRecorder = null;
        let audioChunks = [];
        let stream = null;
        
        // Function to start recording
        window.startRecording = async function() {
            try {
                // Stop any existing recording first
                if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                    mediaRecorder.stop();
                }
                
                // Release any existing stream
                if (stream) {
                    stream.getTracks().forEach(track => track.stop());
                }
                
                // Get new audio stream
                stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                // Collect audio data
                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });
                
                // Process audio when stopped
                mediaRecorder.addEventListener('stop', () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = () => {
                        const base64data = reader.result.split(',')[1];
                        // Store in session storage and notify parent window
                        window.parent.postMessage({
                            type: 'audio_data',
                            audio: base64data
                        }, '*');
                    };
                    
                    // Release resources
                    if (stream) {
                        stream.getTracks().forEach(track => track.stop());
                        stream = null;
                    }
                });
                
                // Start recording
                mediaRecorder.start();
                console.log('Recording started');
                
            } catch (err) {
                console.error('Error accessing microphone:', err);
                alert('Error accessing microphone. Please check your permissions.');
            }
        };
        
        // Function to stop recording
        window.stopRecording = function() {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
                console.log('Recording stopped');
            }
        };
    })();
    </script>
    """
    st.components.v1.html(audio_recorder_js, height=0)

def magic_ai_voice_input():
    """
    Magic Design AI Voice Input component
    Returns the transcribed text if available
    """
    # Initialize session state variables
    if 'magic_recording' not in st.session_state:
        st.session_state.magic_recording = False
    
    if 'magic_recordings' not in st.session_state:
        st.session_state.magic_recordings = []
    
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = None
    
    # Create a custom component for receiving audio data
    if 'audio_data_receiver' not in st.session_state:
        st.session_state.audio_data_receiver = None
        
    # Use a hidden component to receive audio data from JavaScript
    audio_data_receiver = st.empty()
    
    # Add JavaScript to handle audio data communication
    st.markdown("""
    <script>
    // Listen for messages from the audio recorder
    window.addEventListener('message', function(event) {
        const data = event.data;
        if (data && data.type === 'audio_data') {
            // Store in session storage for Streamlit to access on next rerun
            sessionStorage.setItem('recorded_audio_data', data.audio);
            // Force a rerun to process the audio
            window.parent.postMessage({type: 'streamlit:forceRerun'}, '*');
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Check for audio data in session storage
    check_audio_script = """
    <script>
    const audioData = sessionStorage.getItem('recorded_audio_data');
    if (audioData) {
        // Clear from session storage to avoid reprocessing
        sessionStorage.removeItem('recorded_audio_data');
        // Send to Streamlit's session state via the Streamlit API
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: audioData
        }, '*');
    }
    </script>
    """
    st.components.v1.html(check_audio_script, height=0)
    
    # Create container for the component
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create a centered container for the microphone button
        centered_container = st.container()
        with centered_container:
            # Display microphone icon
            mic_icon = "🎤"
            if st.session_state.magic_recording:
                # Use a different color when recording
                st.markdown(f"<div style='text-align: center; font-size: 40px; color: #ff3a3a;'>{mic_icon}</div>", unsafe_allow_html=True)
                st.markdown("<div style='text-align: center; color: #ff3a3a;'>Recording...</div>", unsafe_allow_html=True)
                
                # Show animated recording indicator
                st.progress(0.75)
                
                # Add JavaScript to start recording
                st.components.v1.html("<script>window.startRecording();</script>", height=0)
            else:
                st.markdown(f"<div style='text-align: center; font-size: 40px;'>{mic_icon}</div>", unsafe_allow_html=True)
                st.markdown("<div style='text-align: center;'>Click to record</div>", unsafe_allow_html=True)
                
                # Add JavaScript to stop recording if we were recording before
                if hasattr(st.session_state, 'was_recording') and st.session_state.was_recording:
                    st.components.v1.html("<script>window.stopRecording();</script>", height=0)
                    st.session_state.was_recording = False
        
        # Toggle recording button with better styling
        button_style = """
        <style>
        div[data-testid="stButton"] > button {
            background-color: #3a86ff;
            color: white;
            border-radius: 20px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
        }
        </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)
        
        button_text = "Stop Recording" if st.session_state.magic_recording else "Start Recording"
        if st.button(button_text, key="magic_toggle_recording"):
            # Toggle recording state
            st.session_state.magic_recording = not st.session_state.magic_recording
            
            if st.session_state.magic_recording:
                # Start recording
                st.session_state.magic_start_time = time.time()
                st.session_state.was_recording = True
            else:
                # Stop recording and process
                if hasattr(st.session_state, 'magic_start_time'):
                    duration = time.time() - st.session_state.magic_start_time
                    
                    # Process audio data if available
                    # Get the audio data from the component value
                    component_value = audio_data_receiver.get_component_value()
                    if component_value:
                        # Store it in session state
                        st.session_state.audio_data = component_value
                    
                    if 'audio_data' in st.session_state and st.session_state.audio_data:
                        # Get speech recognition service
                        speech_service = get_speech_recognition_service()
                        
                        # Show processing indicator
                        with st.spinner("Processing audio..."): 
                            try:
                                # Use the real transcription service if API key is available
                                if speech_service.api_key:
                                    transcription = speech_service.transcribe_audio_data(st.session_state.audio_data)
                                else:
                                    # Fall back to simulation if no API key
                                    transcription = speech_service.simulate_transcription(duration)
                            except Exception as e:
                                st.error(f"Error processing audio: {str(e)}")
                                transcription = "Error processing audio. Using simulated response instead."
                                transcription = speech_service.simulate_transcription(duration)
                        
                        # Add to recordings
                        st.session_state.magic_recordings.append({
                            'duration': duration,
                            'timestamp': datetime.now(),
                            'text': transcription
                        })
                        
                        # Clear audio data
                        st.session_state.audio_data = None
                        
                        # Return the latest transcription
                        return st.session_state.magic_recordings[-1]['text']
                    else:
                        # Simulate transcription if no audio data
                        speech_service = get_speech_recognition_service()
                        transcription = speech_service.simulate_transcription(duration)
                        
                        # Add to recordings
                        st.session_state.magic_recordings.append({
                            'duration': duration,
                            'timestamp': datetime.now(),
                            'text': transcription
                        })
                        
                        # Return the latest transcription
                        return st.session_state.magic_recordings[-1]['text']
    
    # Display recording history
    if st.session_state.magic_recordings:
        st.markdown("### Recent Recordings")
        
        for i, recording in enumerate(reversed(st.session_state.magic_recordings[-5:])):
            duration_str = f"{recording['duration']:.1f}s"
            time_str = recording['timestamp'].strftime('%H:%M:%S')
            
            with st.container():
                cols = st.columns([1, 4])
                with cols[0]:
                    st.markdown("🎤")
                with cols[1]:
                    st.markdown(f"**{duration_str}** - {time_str}")
            
            with st.expander("Show transcription"):
                st.write(recording['text'])
    
    return None
