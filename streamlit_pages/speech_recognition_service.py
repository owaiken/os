"""
Speech Recognition Service for Owaiken
Uses OpenAI Whisper API for speech-to-text conversion
"""
import streamlit as st
import tempfile
import os
import base64
import requests
import json
import time
from pathlib import Path
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Security-focused functions for accessing sensitive data
def get_secret(key, default=None):
    """Safely get a secret from Streamlit secrets or environment variables
    
    Prioritizes environment variables over secrets.toml for production security
    """
    try:
        # First try to get from environment variables (more secure for production)
        env_value = os.getenv(key)
        if env_value:
            return env_value
            
        # Fall back to secrets.toml (for development)
        return st.secrets.get(key, default)
    except (FileNotFoundError, AttributeError, Exception):
        return default
        
def sanitize_input(input_data):
    """Sanitize user input to prevent injection attacks"""
    if isinstance(input_data, str):
        # Basic sanitization for strings
        return input_data.replace("<", "&lt;").replace(">", "&gt;")
    return input_data

class SpeechRecognitionService:
    """
    Service for converting speech to text using OpenAI's Whisper API
    """
    def __init__(self):
        # Initialize OpenAI client with security best practices
        try:
            # Try multiple sources for the API key (env vars preferred for production)
            self.api_key = os.getenv("OPENAI_API_KEY") or get_secret("OPENAI_API_KEY")
            
            # Set the API key if available
            if self.api_key:
                openai.api_key = self.api_key
                # Don't log success with actual key values in production
                print("OpenAI API key configured successfully")
            else:
                print("No OpenAI API key found. Speech recognition will use demo mode.")
        except Exception as e:
            # Log error without exposing sensitive details
            print(f"Error initializing API configuration: {type(e).__name__}")
            self.api_key = None
        
        # Create a secure directory for temporary audio files
        # Use a random subdirectory name for each session to prevent conflicts
        random_dir = secrets.token_hex(8)
        self.temp_dir = Path(tempfile.gettempdir()) / f"owaiken_audio_{random_dir}"
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Set secure permissions on the temp directory
        try:
            os.chmod(self.temp_dir, stat.S_IRWXU)  # Owner only permissions (700)
        except Exception as e:
            print(f"Warning: Could not set secure permissions on temp directory: {type(e).__name__}")
    
    def transcribe_audio_data(self, audio_data_base64, language="en"):
        """
        Transcribe audio data using OpenAI's Whisper API with security measures
        
        Args:
            audio_data_base64: Base64 encoded audio data
            language: Language code (default: "en" for English)
            
        Returns:
            Transcribed text or error message
        """
        temp_file = None
        try:
            # Check if API key is available
            if not self.api_key:
                return "Error: API key not configured. Please contact your administrator."
            
            # Validate input
            if not audio_data_base64 or not isinstance(audio_data_base64, str):
                return "Error: Invalid audio data format"
                
            # Limit input size for security (prevent DOS attacks)
            if len(audio_data_base64) > 10 * 1024 * 1024:  # 10MB limit
                return "Error: Audio data exceeds size limit"
            
            try:
                # Decode base64 audio data
                audio_data = base64.b64decode(audio_data_base64)
            except Exception:
                return "Error: Invalid audio data encoding"
            
            # Generate secure random filename
            secure_filename = f"audio_{secrets.token_hex(16)}.wav"
            temp_file = self.temp_dir / secure_filename
            
            # Save to temporary file with secure permissions
            with open(temp_file, "wb") as f:
                f.write(audio_data)
            
            # Set secure permissions
            os.chmod(temp_file, stat.S_IRUSR | stat.S_IWUSR)  # Owner read/write only (600)
            
            # Transcribe using OpenAI Whisper API
            with open(temp_file, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            
            # Get the transcribed text
            transcribed_text = transcript.get("text", "")
            
            # Sanitize output before returning (prevent XSS)
            return sanitize_input(transcribed_text)
        
        except Exception as e:
            # Log the error type but not the full details (could contain sensitive info)
            error_type = type(e).__name__
            print(f"Transcription error: {error_type}")
            return f"Error processing audio: Please try again"
        
        finally:
            # Always clean up temporary file, even if an exception occurred
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass  # Fail silently on cleanup errors
    
    def transcribe_audio_file(self, audio_file_path, language="en"):
        """
        Transcribe audio file using OpenAI's Whisper API
        
        Args:
            audio_file_path: Path to audio file
            language: Language code (default: "en" for English)
            
        Returns:
            Transcribed text or error message
        """
        try:
            # Check if API key is available
            if not self.api_key:
                return "Error: OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
            
            # Check if file exists
            if not os.path.exists(audio_file_path):
                return f"Error: Audio file not found at {audio_file_path}"
            
            # Transcribe using OpenAI Whisper API
            with open(audio_file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            
            return transcript.get("text", "")
        
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"
    
    def simulate_transcription(self, duration):
        """
        Simulate transcription for testing purposes
        
        Args:
            duration: Duration of the audio in seconds
            
        Returns:
            Simulated transcribed text
        """
        # Simulate different responses based on duration
        if duration < 2:
            return "Hello there."
        elif duration < 5:
            return "I'd like to create a workflow for automating email responses."
        else:
            return "Please create an N8N workflow that monitors my Gmail inbox and automatically categorizes emails based on their content. When an important email arrives, I want to receive a notification on my phone."


# Create a singleton instance
speech_recognition_service = SpeechRecognitionService()

def get_speech_recognition_service():
    """
    Get the speech recognition service instance
    """
    return speech_recognition_service


def transcribe_audio(audio_data):
    """
    Transcribe audio data using the speech recognition service
    
    Args:
        audio_data: Audio data to transcribe
        
    Returns:
        Transcribed text or error message
    """
    try:
        # Get the speech recognition service
        service = get_speech_recognition_service()
        
        # Check if we have audio data
        if not audio_data:
            return None
        
        # Convert audio data to base64
        import base64
        audio_bytes = audio_data
        base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        
        # Check if we're in demo mode (no API key)
        if not service.api_key:
            # Return a simulated response
            import time
            # Simulate processing time
            time.sleep(1)
            return service.simulate_transcription(5)
        
        # Transcribe the audio
        return service.transcribe_audio_data(base64_audio)
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        # Return a friendly error message
        return f"Sorry, I couldn't transcribe the audio. Error: {str(e)}"
