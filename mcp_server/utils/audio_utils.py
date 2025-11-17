import os
import pathlib
from gtts import gTTS
import uuid
import pygame

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
        self.temp_tts_dir = pathlib.Path(".temp/text_to_speech")
        self.temp_tts_dir.mkdir(parents=True, exist_ok=True)

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

            tts = gTTS(text=text, lang="en", slow=False)
            tts.save(str(file_path))

            return str(file_path)
        except Exception as e:
            print(f"Error generating TTS: {str(e)}")
            raise

    def play_audio(self, audio_file: str):
        """
        Play audio file

        Args:
            audio_file: Path to the audio file
        """
        try:
            print(f"Playing audio file: {audio_file}")
                
            # Convert to absolute path for audioplayer
            audio_path = pathlib.Path(audio_file).resolve()
            pygame.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing audio: {str(e)}")
            raise
        finally:
            pygame.quit()
            os.remove(audio_file)
            print(f"Audio file removed: {audio_file}")
