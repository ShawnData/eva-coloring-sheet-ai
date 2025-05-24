import gradio as gr

class VoiceInterface:
    def __init__(self, voice_agent):
        """
        Initialize the voice interface with a voice agent.
        
        Args:
            voice_agent: An instance of VoiceAgent that handles the voice processing
        """
        self.voice_agent = voice_agent
        
    def process_voice(self):
        """Process voice input using the voice agent"""
        return self.voice_agent.process_voice_input()
    
    def create_interface(self):
        """Create and return the Gradio interface"""
        interface = gr.Interface(
            fn=self.process_voice,
            inputs=None,
            outputs="text",
            title="Eva's Coloring Sheet AI - Voice Input",
            description="Click the button below to start recording your voice input.",
            allow_flagging="never"
        )
        return interface
    
    def launch(self):
        """Create and launch the Gradio interface"""
        interface = self.create_interface()
        interface.launch() 