import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
from crewai import Agent, Task, Crew
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
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = openai.OpenAI(api_key=api_key)
        
        # Audio recording parameters
        self.sample_rate = 44100
        self.channels = 1
        self.duration = 5  # seconds
        
    def record_audio(self):
        """Record audio from the default microphone"""
        try:
            print("Recording...")
            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels
            )
            sd.wait()
            print("Recording finished")
            return recording
        except Exception as e:
            print(f"Error recording audio: {str(e)}")
            raise
    
    def save_audio(self, audio_data, filename="temp_recording.wav"):
        """
        Save the audio data to a file
        
        Args:
            audio_data: numpy array containing the audio data
            filename: name of the file to save the audio to
        """
        try:
            # Ensure the audio data is in the correct format
            if isinstance(audio_data, tuple):
                sample_rate, audio_data = audio_data
            else:
                sample_rate = self.sample_rate
                
            # Normalize audio data if needed
            if audio_data.dtype != np.int16:
                audio_data = (audio_data * 32767).astype(np.int16)
                
            write(filename, sample_rate, audio_data)
            return filename
        except Exception as e:
            print(f"Error saving audio: {str(e)}")
            raise
    
    def transcribe_audio(self, audio_file):
        """
        Transcribe the audio file using OpenAI's Whisper API
        
        Args:
            audio_file: path to the audio file to transcribe
        """
        try:
            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"Audio file not found: {audio_file}")
                
            with open(audio_file, "rb") as file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file
                )
            return transcript.text
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            raise
    
    def process_input(self, text):
        """
        Process text input and generate a response using the agent
        
        Args:
            text: The input text to process
            
        Returns:
            str: The agent's response
        """
        try:
            # Create a task for the agent
            task = Task(
                description=f"Respond to the following input from a child: {text}",
                agent=self.agent,
                expected_output="A friendly and engaging response that is appropriate for children"
            )
            
            # Create a crew with the agent and task
            crew = Crew(
                agents=[self.agent],
                tasks=[task],
                verbose=True
            )
            
            # Get the agent's response
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            print(f"Error processing input: {str(e)}")
            raise
    
    def process_voice_input(self):
        """Process voice input and return transcription"""
        try:
            # Record audio
            recording = self.record_audio()
            
            # Save audio
            audio_file = self.save_audio(recording)
            
            # Transcribe audio
            transcription = self.transcribe_audio(audio_file)
            
            # Clean up temporary file
            if os.path.exists(audio_file):
                os.remove(audio_file)
            
            return transcription
        except Exception as e:
            print(f"Error processing voice input: {str(e)}")
            raise 