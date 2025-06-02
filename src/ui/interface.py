import os
import openai
import gradio as gr
from typing import List, Dict
from src.utils.audio_utils import AudioUtils
from src.crews.coloring_sheet_crew import ColoringSheetCrew
from crewai.crew import CrewOutput

class ColoringSheetInterface:
    def __init__(self, ai_crew: ColoringSheetCrew):
        self.ai_crew = ai_crew
        self.audio_utils = AudioUtils()
        self.chat_history: List[Dict[str, str]] = []
                
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.openai_client = openai.OpenAI(api_key=api_key)
        
    def process_voice(self, audio, history):
        if audio is None:
            return history, "No audio input detected. Please record your voice.", None  # Added None for image output
            
        sample_rate, audio_data = audio
        # Save the audio data to a temporary file
        audio_file = self.audio_utils.save_audio(audio_data)
        
        # Transcribe the audio
        try:
            transcription = self.audio_utils.transcribe_audio(audio_file, self.openai_client)
            # Add user's voice input to history
            history.append({"role": "user", "content": f"(Voice) {transcription}"})
            
            # Get agent's response
            response: CrewOutput = self.ai_crew.kickoff(inputs={"transcription": transcription})
            if response:
                # Assuming response is a dict with 'message' and 'image_url' keys
                message = str(response.get('message', response))  # Fallback to full response if not dict
                image_url = response.get('image_url', None)  # Get image URL if available
                history.append({"role": "assistant", "content": message})
                file_path = self.audio_utils.generate_tts(message)
                return history, file_path, image_url
            else:
                history.append({"role": "system", "content": "Sorry, I couldn't generate a response. Please try again."})
                return history, None, None
            
        except Exception as e:
            error_msg = f"Error processing audio: {str(e)}"
            history.append({"role": "system", "content": error_msg})
            return history, error_msg, None
    
    def create_interface(self):
        """Create and return the Gradio interface"""
        with gr.Blocks(title="Eva's Coloring Sheet AI - Chat Interface") as interface:
            gr.Markdown("# Eva's Coloring Sheet AI")
            gr.Markdown("Chat with Eva using voice or text input!")
            
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        value=[],
                        label="Chat History",
                        height=600,
                        type="messages"  # Using the new messages format
                    )
                    
                    with gr.Row():
                        with gr.Column(scale=2):
                            # Combined input area
                            with gr.Group():
                                audio_input = gr.Audio(
                                    type="numpy",
                                    streaming=False,
                                    label="Voice Input",
                                    sources=["microphone"],
                                    interactive=True,
                                    elem_id="mic-button",
                                )
                
                # Add image display column
                with gr.Column(scale=2):
                    image_output = gr.Image(
                        label="Generated Coloring Sheet",
                        type="filepath",  # Can accept both URLs and file paths
                        interactive=False,
                        height=500,
                    )
            
            audio_output = gr.Audio(label="TTS", type="filepath", visible=False, interactive=False, autoplay=True)
            
            audio_input.change(
                self.process_voice,
                inputs=[audio_input, chatbot],
                outputs=[chatbot, audio_output, image_output]  # Added image_output
            )
            
        return interface
    
    def launch(self):
        """Create and launch the Gradio interface"""
        interface = self.create_interface()
        interface.launch() 