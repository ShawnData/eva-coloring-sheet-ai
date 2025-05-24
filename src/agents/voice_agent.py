import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
from crewai import Agent
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class VoiceAgent:
    def __init__(self):
        self.agent = Agent(
            role='Voice Interaction Specialist',
            goal='Facilitate natural voice-based interaction with children',
            backstory="""You are a friendly, patient voice interaction specialist who excels at 
            communicating with children. You have a natural ability to understand and adapt to 
            different age groups, making complex concepts simple and engaging.""",
            verbose=True,
            allow_delegation=True
        )
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Audio recording parameters
        self.sample_rate = 44100
        self.channels = 1
        self.duration = 5  # seconds
        
    def record_audio(self):
        """Record audio from the default microphone"""
        print("Recording...")
        recording = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels
        )
        sd.wait()
        print("Recording finished")
        return recording
    
    def save_audio(self, recording, filename="temp_recording.wav"):
        """Save the recorded audio to a file"""
        write(filename, self.sample_rate, recording)
        return filename
    
    def transcribe_audio(self, audio_file):
        """Transcribe the audio file using OpenAI's Whisper API"""
        with open(audio_file, "rb") as file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=file
            )
        return transcript.text
    
    def process_voice_input(self):
        """Process voice input and return transcription"""
        # Record audio
        recording = self.record_audio()
        
        # Save audio
        audio_file = self.save_audio(recording)
        
        # Transcribe audio
        transcription = self.transcribe_audio(audio_file)
        
        # Clean up temporary file
        os.remove(audio_file)
        
        return transcription 