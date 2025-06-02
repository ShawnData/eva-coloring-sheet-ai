import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import pathlib
from datetime import datetime
import openai
from typing import Optional
from gtts import gTTS
import uuid

class AudioUtils:
    def __init__(self, sample_rate: int = 44100, channels: int = 1, duration: int = 5):
        """
        Initialize AudioUtils with recording parameters
        
        Args:
            sample_rate: Sample rate for audio recording
            channels: Number of audio channels
            duration: Recording duration in seconds
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration
        
        # Create temp directories
        self.temp_audio_dir = pathlib.Path(".temp/agent_save_audio")
        self.temp_tts_dir = pathlib.Path(".temp/text_to_speech")
        self.temp_audio_dir.mkdir(parents=True, exist_ok=True)
        self.temp_tts_dir.mkdir(parents=True, exist_ok=True)


    def save_audio(self, audio_data: np.ndarray, filename: Optional[str] = None) -> str:
        """
        Save audio data to a file
        
        Args:
            audio_data: Numpy array containing the audio data
            filename: Optional name for the audio file
            
        Returns:
            str: Path to the saved audio file
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.wav"
            
            if isinstance(audio_data, tuple):
                sample_rate, audio_data = audio_data
            else:
                sample_rate = self.sample_rate
                
            if audio_data.dtype != np.int16:
                audio_data = (audio_data * 32767).astype(np.int16)
            
            file_path = self.temp_audio_dir / filename
            write(str(file_path), sample_rate, audio_data)
            return str(file_path)
        except Exception as e:
            print(f"Error saving audio: {str(e)}")
            raise

    def transcribe_audio(self, audio_file: str, client: openai.OpenAI) -> str:
        """
        Transcribe audio file using OpenAI's Whisper API
        
        Args:
            audio_file: Path to the audio file
            client: OpenAI client instance
            
        Returns:
            str: Transcribed text
        """
        try:
            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"Audio file not found: {audio_file}")
                
            with open(audio_file, "rb") as file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file
                )
            return transcript.text
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            raise
        finally:
            try:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            except Exception as e:
                print(f"Error deleting audio file: {str(e)}")

    def generate_tts(self, text: str) -> str:
        """
        Generate text-to-speech audio file
        
        Args:
            text: Text to convert to speech
            
        Returns:
            str: Path to the generated audio file
        """
        try:
            filename = f"tts_{uuid.uuid4().hex}.mp3"
            file_path = self.temp_tts_dir / filename
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(file_path))
            
            return str(file_path)
        except Exception as e:
            print(f"Error generating TTS: {str(e)}")
            raise 