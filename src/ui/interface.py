import os
import gradio as gr
import numpy as np
from typing import Tuple, Optional
from src.crews.coloring_sheet_crew import ColoringSheetCrew
from src.utils.audio_utils import AudioUtils

class ColoringSheetInterface:
    """
    Gradio interface for the Eva Coloring Sheet AI system
    Handles voice input, text-to-speech output, and image display
    """
    
    def __init__(self, crew: ColoringSheetCrew):
        """
        Initialize the interface
        
        Args:
            crew: The ColoringSheetCrew instance to handle voice processing
        """
        self.crew = crew
        self.audio_utils = AudioUtils()
        self.interface = self._create_interface()
    
    def _create_interface(self) -> gr.Blocks:
        """Create the Gradio interface"""
        
        with gr.Blocks(
            title="Eva Coloring Sheet AI",
            theme=gr.themes.Soft(),
            css="""
            .gradio-container {
                max-width: 1200px !important;
                margin: 0 auto !important;
            }
            .chat-message {
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
                max-width: 80%;
            }
            .user-message {
                background-color: #e3f2fd;
                margin-left: auto;
                text-align: right;
            }
            .assistant-message {
                background-color: #f5f5f5;
                margin-right: auto;
            }
            """
        ) as interface:
            
            # Header
            gr.Markdown(
                """
                # 🎨 Eva Coloring Sheet AI
                ### Create beautiful coloring sheets with your voice!
                
                **How to use:**
                1. Click the microphone button and speak your request
                2. Say something like "I want a cat coloring sheet" or "Make me a flower drawing"
                3. Eva will respond with voice and create your coloring sheet!
                """
            )
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Voice input section
                    gr.Markdown("### 🎤 Voice Input")
                    audio_input = gr.Audio(
                        type="numpy",
                        streaming=False,
                        label="Click to record your voice",
                        sources=["microphone"],
                        interactive=True,
                        height=200
                    )
                    
                    # Manual text input as fallback
                    gr.Markdown("### 📝 Or type your request")
                    text_input = gr.Textbox(
                        label="Type your request here",
                        placeholder="e.g., I want a cat coloring sheet",
                        lines=2
                    )
                    
                    # Submit button for text input
                    submit_btn = gr.Button("Submit Request", variant="primary")
                    
                    # Status indicator
                    status = gr.Textbox(
                        label="Status",
                        value="Ready to help! Click the microphone or type your request.",
                        interactive=False
                    )
                
                with gr.Column(scale=2):
                    # Chat history
                    gr.Markdown("### 💬 Conversation")
                    chat_history = gr.HTML(
                        value="<div style='height: 400px; overflow-y: auto; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>"
                              "<p style='text-align: center; color: #666;'>Start a conversation with Eva!</p></div>",
                        label="Chat History"
                    )
                    
                    # Generated image
                    gr.Markdown("### 🖼️ Your Coloring Sheet")
                    image_output = gr.Image(
                        label="Generated Coloring Sheet",
                        height=400,
                        show_label=True
                    )
            
            # Event handlers
            audio_input.change(
                fn=self._handle_voice_input,
                inputs=[audio_input],
                outputs=[chat_history, image_output, status, audio_input]
            )
            
            submit_btn.click(
                fn=self._handle_text_input,
                inputs=[text_input],
                outputs=[chat_history, image_output, status, text_input]
            )
            
            # Enter key support for text input
            text_input.submit(
                fn=self._handle_text_input,
                inputs=[text_input],
                outputs=[chat_history, image_output, status, text_input]
            )
        
        return interface
    
    def _handle_voice_input(self, audio: Optional[Tuple[int, np.ndarray]]) -> Tuple[str, Optional[np.ndarray], str, None]:
        """
        Handle voice input from microphone
        
        Args:
            audio: Tuple of (sample_rate, audio_data) or None
            
        Returns:
            Tuple of (chat_history_html, image_data, status_message, reset_audio)
        """
        if audio is None:
            return self._get_chat_html(), None, "No audio detected. Please try again.", None
        
        try:
            # Update status
            status_msg = "Processing your voice input..."
            
            # Transcribe audio
            sample_rate, audio_data = audio
            audio_file = self.audio_utils.save_audio((sample_rate, audio_data))
            
            # Get OpenAI client from crew
            openai_client = self.crew.voice_assistant.openai_client
            transcription = self.audio_utils.transcribe_audio(audio_file, openai_client)
            
            if not transcription.strip():
                return self._get_chat_html(), None, "I couldn't hear what you said. Please try again.", None
            
            # Process with crew
            result = self.crew.process_voice_input(transcription)
            
            # Generate TTS for response
            tts_file = self.audio_utils.generate_tts(result['message'])
            
            # Update chat history
            chat_html = self._add_to_chat_history(transcription, result['message'], tts_file)
            
            # Update status
            if result.get('image_url'):
                status_msg = f"✅ Created your coloring sheet! Listen to Eva's response above."
            else:
                status_msg = f"✅ Eva responded! Listen to the message above."
            
            return chat_html, result.get('image_url'), status_msg, None
            
        except Exception as e:
            error_msg = f"Sorry, something went wrong: {str(e)}"
            return self._get_chat_html(), None, error_msg, None
    
    def _handle_text_input(self, text: str) -> Tuple[str, Optional[np.ndarray], str, str]:
        """
        Handle text input
        
        Args:
            text: User's text input
            
        Returns:
            Tuple of (chat_history_html, image_data, status_message, reset_text)
        """
        if not text.strip():
            return self._get_chat_html(), None, "Please enter your request.", ""
        
        try:
            # Update status
            status_msg = "Processing your request..."
            
            # Process with crew
            result = self.crew.process_voice_input(text)
            
            # Generate TTS for response
            tts_file = self.audio_utils.generate_tts(result['message'])
            
            # Update chat history
            chat_html = self._add_to_chat_history(text, result['message'], tts_file)
            
            # Update status
            if result.get('image_url'):
                status_msg = f"✅ Created your coloring sheet! Listen to Eva's response above."
            else:
                status_msg = f"✅ Eva responded! Listen to the message above."
            
            return chat_html, result.get('image_url'), status_msg, ""
            
        except Exception as e:
            error_msg = f"Sorry, something went wrong: {str(e)}"
            return self._get_chat_html(), None, error_msg, text
    
    def _get_chat_html(self) -> str:
        """Get the current chat history HTML"""
        return "<div style='height: 400px; overflow-y: auto; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>" \
               "<p style='text-align: center; color: #666;'>Start a conversation with Eva!</p></div>"
    
    def _add_to_chat_history(self, user_input: str, assistant_response: str, tts_file: str) -> str:
        """
        Add a new exchange to the chat history
        
        Args:
            user_input: What the user said
            assistant_response: What Eva responded
            tts_file: Path to the TTS audio file
            
        Returns:
            Updated chat history HTML
        """
        # Create audio player for TTS
        audio_html = f"""
        <audio controls style="width: 100%; margin: 5px 0;">
            <source src="file/{tts_file}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        """
        
        # Create the new chat exchange
        new_exchange = f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {user_input}
        </div>
        <div class="chat-message assistant-message">
            <strong>Eva:</strong> {assistant_response}
            {audio_html}
        </div>
        """
        
        # Get current chat history and add new exchange
        current_html = self._get_chat_html()
        # Remove the placeholder message if it exists
        if "Start a conversation with Eva!" in current_html:
            current_html = current_html.replace(
                "<p style='text-align: center; color: #666;'>Start a conversation with Eva!</p>",
                ""
            )
        
        # Add new exchange
        updated_html = current_html.replace("</div>", f"{new_exchange}</div>")
        
        return updated_html
    
    def launch(self, **kwargs):
        """Launch the Gradio interface"""
        return self.interface.launch(**kwargs) 