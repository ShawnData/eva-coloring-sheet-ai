import gradio as gr
from typing import List, Dict
from gtts import gTTS
import tempfile
import pygame
import os
import uuid

# Initialize pygame mixer for playback
pygame.mixer.init()

def text_to_speech(text: str):
    """
    Convert text to speech and play it through speakers.
    Save the audio file in a local .temp/test_to_speech folder and delete after playback.
    """
    try:
        temp_dir = os.path.join(os.getcwd(), '.temp/test_to_speech')
        os.makedirs(temp_dir, exist_ok=True)
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        file_path = os.path.join(temp_dir, filename)
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(file_path)
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove(file_path)
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")

class VoiceInterface:
    def __init__(self, voice_agent):
        """
        Initialize the voice interface with a voice agent.
        
        Args:
            voice_agent: An instance of VoiceAgent that handles the voice processing
        """
        self.voice_agent = voice_agent
        self.chat_history: List[Dict[str, str]] = []
        
    def process_voice(self, audio, history):
        """
        Process voice input using the voice agent
        
        Args:
            audio: Tuple of (sample_rate, audio_data) from Gradio's audio component
            history: List of previous chat messages
        """
        if audio is None:
            return history, "No audio input detected. Please record your voice."
            
        sample_rate, audio_data = audio
        # Save the audio data to a temporary file
        audio_file =self.voice_agent.save_audio(audio_data)
        
        # Transcribe the audio
        try:
            transcription = self.voice_agent.transcribe_audio(audio_file)
            # Add user's voice input to history
            history.append({"role": "user", "content": f"(Voice) {transcription}"})
            
            # Get agent's response
            response = self.voice_agent.process_input(transcription)
            if response:
                history.append({"role": "assistant", "content": response})
                text_to_speech(response)
            else:
                history.append({"role": "system", "content": "Sorry, I couldn't generate a response. Please try again."})
            
            return history, ""
        except Exception as e:
            error_msg = f"Error processing audio: {str(e)}"
            history.append({"role": "system", "content": error_msg})
            return history, error_msg
    
    def process_text(self, text, history):
        """
        Process text input using the voice agent
        
        Args:
            text: Text input from the user
            history: List of previous chat messages
        """
        if not text.strip():
            return history, "Please enter some text."
            
        try:
            # Add user's text input to history
            history.append({"role": "user", "content": text})
            
            # Get agent's response
            response = self.voice_agent.process_input(text)
            if response:
                history.append({"role": "assistant", "content": response})
                text_to_speech(response)
            else:
                history.append({"role": "system", "content": "Sorry, I couldn't generate a response. Please try again."})
            
            return history, ""
        except Exception as e:
            error_msg = f"Error processing text: {str(e)}"
            history.append({"role": "system", "content": error_msg})
            return history, error_msg
    
    def create_interface(self):
        """Create and return the Gradio interface"""
        with gr.Blocks(title="Eva's Coloring Sheet AI - Chat Interface") as interface:
            gr.Markdown("# Eva's Coloring Sheet AI")
            gr.Markdown("Chat with Eva using voice or text input!")
            
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        value=[],
                        elem_id="chatbot",
                        height=600,
                        type="messages"  # Using the new messages format
                    )
                    
                    with gr.Row():
                        with gr.Column(scale=4):
                            text_input = gr.Textbox(
                                placeholder="Type your message here...",
                                show_label=False,
                                container=False
                            )
                        with gr.Column(scale=1):
                            text_submit = gr.Button("Send")
                    
                    with gr.Row():
                        audio_input = gr.Audio(
                            type="numpy",
                            streaming=False,
                            label="Voice Input",
                            sources=["microphone"],  # Only allow microphone input
                            interactive=True
                        )
                        audio_submit = gr.Button("Send Voice")
            
            # Set up event handlers
            text_submit.click(
                self.process_text,
                inputs=[text_input, chatbot],
                outputs=[chatbot, text_input]
            )
            
            text_input.submit(
                self.process_text,
                inputs=[text_input, chatbot],
                outputs=[chatbot, text_input]
            )
            
            audio_submit.click(
                self.process_voice,
                inputs=[audio_input, chatbot],
                outputs=[chatbot, audio_input]
            )
            
        return interface
    
    def launch(self):
        """Create and launch the Gradio interface"""
        interface = self.create_interface()
        interface.launch() 