"""
Magic Design UI Components for Streamlit
Implements UI components inspired by magic.design
"""
import streamlit as st
import base64
import json
import time
from datetime import datetime

def apply_magic_design_styles():
    """
    Apply Magic Design styling to Streamlit
    """
    st.markdown("""
    <style>
    /* Magic Design Voice Input Component */
    .magic-voice-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
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
        position: relative;
        overflow: hidden;
    }
    
    .magic-voice-button:hover {
        transform: scale(1.05);
        background-color: #333;
    }
    
    .magic-voice-button.recording {
        background-color: #ff3a3a;
        box-shadow: 0 0 0 rgba(255, 58, 58, 0.4);
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
    
    .magic-voice-icon {
        width: 24px;
        height: 24px;
        fill: #fff;
        transition: all 0.3s ease;
    }
    
    .magic-voice-button.recording .magic-voice-icon {
        fill: #fff;
    }
    
    .magic-voice-ripple {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.1);
        transform: scale(0);
        animation: ripple 1s linear infinite;
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        100% {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    .magic-voice-status {
        margin-top: 12px;
        font-size: 14px;
        color: #888;
        transition: all 0.3s ease;
    }
    
    .magic-voice-status.recording {
        color: #ff3a3a;
    }
    
    .magic-voice-timer {
        font-size: 12px;
        color: #888;
        margin-top: 4px;
    }
    
    .magic-voice-recordings {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 16px;
        width: 100%;
        justify-content: center;
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
    
    .magic-voice-recording-icon {
        width: 16px;
        height: 16px;
        fill: #3a86ff;
    }
    
    .magic-voice-recording-info {
        display: flex;
        flex-direction: column;
    }
    
    .magic-voice-recording-duration {
        font-weight: bold;
    }
    
    .magic-voice-recording-time {
        font-size: 10px;
        color: #888;
    }
    
    /* Voice visualization */
    .magic-voice-visualization {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 40px;
        width: 100%;
        margin-top: 12px;
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
    .magic-voice-bar:nth-child(6) { animation-delay: 0.3s; }
    .magic-voice-bar:nth-child(7) { animation-delay: 0.2s; }
    .magic-voice-bar:nth-child(8) { animation-delay: 0.1s; }
    .magic-voice-bar:nth-child(9) { animation-delay: 0.0s; }
    </style>
    """, unsafe_allow_html=True)

def ai_voice_input():
    """
    AI Voice Input component inspired by magic.design
    Returns the transcribed text if available
    """
    # Initialize session state variables
    if 'magic_voice_recording' not in st.session_state:
        st.session_state.magic_voice_recording = False
    
    if 'magic_voice_recordings' not in st.session_state:
        st.session_state.magic_voice_recordings = []
    
    if 'magic_voice_start_time' not in st.session_state:
        st.session_state.magic_voice_start_time = None
    
    if 'magic_voice_transcription' not in st.session_state:
        st.session_state.magic_voice_transcription = None
    
    # Create container for the voice input component
    voice_container = st.container()
    
    with voice_container:
        # Create the HTML for the voice input component
        recording_class = "recording" if st.session_state.magic_voice_recording else ""
        recording_status = "Recording..." if st.session_state.magic_voice_recording else "Click to record"
        
        # Calculate recording time if recording
        timer_html = ""
        if st.session_state.magic_voice_recording and st.session_state.magic_voice_start_time:
            elapsed = time.time() - st.session_state.magic_voice_start_time
            timer_html = f'<div class="magic-voice-timer">{elapsed:.1f}s</div>'
        
        # Create ripple effect if recording
        ripple_html = '<div class="magic-voice-ripple"></div>' if st.session_state.magic_voice_recording else ''
        
        # Create visualization if recording
        visualization_html = ""
        if st.session_state.magic_voice_recording:
            visualization_html = """
            <div class="magic-voice-visualization">
                <div class="magic-voice-bar"></div>
                <div class="magic-voice-bar"></div>
                <div class="magic-voice-bar"></div>
                <div class="magic-voice-bar"></div>
                <div class="magic-voice-bar"></div>
                <div class="magic-voice-bar"></div>
                <div class="magic-voice-bar"></div>
                <div class="magic-voice-bar"></div>
                <div class="magic-voice-bar"></div>
            </div>
            """
        
        # Create recordings display
        recordings_html = ""
        if st.session_state.magic_voice_recordings:
            recordings_html = '<div class="magic-voice-recordings">'
            for recording in st.session_state.magic_voice_recordings[-5:]:  # Show last 5 recordings
                duration_str = f"{recording['duration']:.1f}s"
                time_str = time.strftime('%H:%M:%S', recording['timestamp'])
                
                recording_html = f'''
                <div class="magic-voice-recording">
                    <svg class="magic-voice-recording-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                        <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                    </svg>
                    <div class="magic-voice-recording-info">
                        <span class="magic-voice-recording-duration">{duration_str}</span>
                        <span class="magic-voice-recording-time">{time_str}</span>
                    </div>
                </div>
                '''
                recordings_html += recording_html
            recordings_html += '</div>'
        
        # Assemble the full HTML
        voice_html = f"""
        <div class="magic-voice-container">
            <button id="magic-voice-button" class="magic-voice-button {recording_class}" onclick="toggleRecording()">
                {ripple_html}
                <svg class="magic-voice-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                </svg>
            </button>
            <div class="magic-voice-status {recording_class}">{recording_status}</div>
            {timer_html}
            {visualization_html}
            {recordings_html}
        </div>
        
        <script>
        // JavaScript for voice recording
        let mediaRecorder;
        let audioChunks = [];
        let startTime;
        
        function toggleRecording() {
            const button = document.getElementById('magic-voice-button');
            const isRecording = button.classList.contains('recording');
            
            if (!isRecording) {
                startRecording();
            } else {
                stopRecording();
            }
        }
        
        async function startRecording() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                startTime = Date.now();
                
                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });
                
                mediaRecorder.addEventListener('stop', () => {
                    const duration = (Date.now() - startTime) / 1000;
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = () => {
                        const base64data = reader.result.split(',')[1];
                        sendToStreamlit({
                            action: 'recording_stopped',
                            duration: duration,
                            audioData: base64data
                        });
                    };
                    
                    // Stop all tracks
                    stream.getTracks().forEach(track => track.stop());
                });
                
                // Start recording
                mediaRecorder.start();
                sendToStreamlit({
                    action: 'recording_started'
                });
                
            } catch (err) {
                console.error('Error accessing microphone:', err);
                alert('Error accessing microphone. Please check your permissions.');
            }
        }
        
        function stopRecording() {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
        }
        
        function sendToStreamlit(data) {
            const stringData = JSON.stringify(data);
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: stringData
            }, '*');
        }
        </script>
        """
        
        # Render the component
        component_value = st.components.v1.html(voice_html, height=200)
        
        # Process component value if available
        if component_value:
            try:
                data = json.loads(component_value)
                
                if data.get('action') == 'recording_started':
                    st.session_state.magic_voice_recording = True
                    st.session_state.magic_voice_start_time = time.time()
                    st.experimental_rerun()
                
                elif data.get('action') == 'recording_stopped':
                    # Add recording to history
                    duration = data.get('duration', 0)
                    st.session_state.magic_voice_recordings.append({
                        'duration': duration,
                        'timestamp': time.localtime()
                    })
                    
                    # Process audio data
                    audio_data = data.get('audioData')
                    if audio_data:
                        # In a real implementation, send to a speech-to-text service
                        # For now, simulate a response
                        time.sleep(1)  # Simulate processing
                        st.session_state.magic_voice_transcription = "This is a simulated voice transcription from Magic Design."
                    
                    # Reset recording state
                    st.session_state.magic_voice_recording = False
                    st.session_state.magic_voice_start_time = None
                    st.experimental_rerun()
            
            except Exception as e:
                st.error(f"Error processing voice input: {str(e)}")
    
    # Return the transcription if available
    transcription = st.session_state.magic_voice_transcription
    if transcription:
        # Reset transcription for next use
        st.session_state.magic_voice_transcription = None
        return transcription
    
    return None
