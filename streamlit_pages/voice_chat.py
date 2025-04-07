"""
Voice chat functionality for Owaiken
"""
import streamlit as st
import json
import base64
import time
from datetime import datetime
from streamlit_pages.speech_recognition_service import get_speech_recognition_service

def init_voice_chat():
    """
    Initialize voice chat functionality in session state
    """
    if 'voice_recording' not in st.session_state:
        st.session_state.voice_recording = False
    
    if 'voice_data' not in st.session_state:
        st.session_state.voice_data = None

def toggle_recording():
    """
    Toggle voice recording state
    """
    st.session_state.voice_recording = not st.session_state.voice_recording
    
    # Reset voice data when starting a new recording
    if st.session_state.voice_recording:
        st.session_state.voice_data = None

def process_audio_data(audio_data):
    """
    Process the received audio data
    Returns the transcribed text
    """
    # Get speech recognition service
    speech_service = get_speech_recognition_service()
    
    try:
        # Use the real transcription service if API key is available
        if speech_service.api_key:
            transcription = speech_service.transcribe_audio_data(audio_data)
        else:
            # Fall back to simulation if no API key
            transcription = speech_service.simulate_transcription(3.0)  # Use default duration
            
        return transcription
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return "Error processing audio. Using simulated response instead."

def voice_recorder_component():
    """
    Create a voice recorder component using HTML/JS
    """
    # JavaScript for recording audio
    recorder_js = """
    const recordButton = document.getElementById('voice-record-button');
    const recordingIndicator = document.getElementById('recording-indicator');
    const voiceWaves = document.getElementById('voice-waves');
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    
    // Function to send data to Streamlit
    function sendDataToStreamlit(audioData) {
        const data = {
            audioData: audioData
        };
        window.parent.postMessage({
            type: 'voice-data',
            data: JSON.stringify(data)
        }, '*');
    }
    
    // Function to toggle recording state
    function toggleRecording() {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    }
    
    // Function to start recording
    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });
            
            mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = () => {
                    const base64data = reader.result.split(',')[1];
                    sendDataToStreamlit(base64data);
                };
                
                // Reset recording state
                isRecording = false;
                recordButton.classList.remove('recording');
                recordingIndicator.style.display = 'none';
                voiceWaves.style.display = 'none';
                
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            });
            
            // Start recording
            mediaRecorder.start();
            isRecording = true;
            recordButton.classList.add('recording');
            recordingIndicator.style.display = 'block';
            voiceWaves.style.display = 'flex';
            
        } catch (err) {
            console.error('Error accessing microphone:', err);
            alert('Error accessing microphone. Please check your permissions.');
        }
    }
    
    // Function to stop recording
    function stopRecording() {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
        }
    }
    
    // Add event listener to the record button
    recordButton.addEventListener('click', toggleRecording);
    
    // Listen for messages from Streamlit
    window.addEventListener('message', function(event) {
        if (event.data.type === 'toggle-recording') {
            toggleRecording();
        }
    });
    """
    
    # HTML for the voice recorder
    recorder_html = """
    <div class="voice-recorder-container">
        <button id="voice-record-button" class="openmanus-voice-button">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" fill="#3a86ff"/>
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" fill="#3a86ff"/>
            </svg>
        </button>
        <div id="recording-indicator" style="display: none; color: #ff3a3a; margin-top: 5px;">Recording...</div>
        <div id="voice-waves" class="voice-waves" style="display: none;">
            <div class="voice-wave"></div>
            <div class="voice-wave"></div>
            <div class="voice-wave"></div>
            <div class="voice-wave"></div>
            <div class="voice-wave"></div>
        </div>
    </div>
    
    <script>
    """ + recorder_js + """
    </script>
    """
    
    # Render the HTML component
    st.components.v1.html(recorder_html, height=100)
    
    # Handle messages from the component
    if st.session_state.voice_recording:
        st.markdown('<div style="color: #ff3a3a;">Recording...</div>', unsafe_allow_html=True)
    
    # Process received audio data
    if st.session_state.voice_data:
        try:
            audio_data = st.session_state.voice_data
            transcription = process_audio_data(audio_data)
            
            # Display the transcription
            st.markdown(f"**Transcription:** {transcription}")
            
            # Create audio playback
            audio_bytes = base64.b64decode(audio_data)
            st.audio(audio_bytes, format="audio/wav")
            
            # Reset voice data after processing
            st.session_state.voice_data = None
            
            return transcription
        except Exception as e:
            st.error(f"Error processing audio: {str(e)}")
    
    return None

def handle_voice_message(message):
    """
    Handle a voice message by sending it to the appropriate service
    """
    if not message:
        return
    
    # In a real implementation, this would send the message to the AI service
    # For now, we'll simulate a response
    time.sleep(1)  # Simulate processing time
    
    return f"Response to: {message}"
