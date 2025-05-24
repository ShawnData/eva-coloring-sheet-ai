from src.agents.voice_agent import VoiceAgent
from src.ui.voice_interface import VoiceInterface

def main():
    # Initialize the voice agent
    voice_agent = VoiceAgent()
    
    # Create and launch the voice interface
    interface = VoiceInterface(voice_agent)
    interface.launch()

if __name__ == "__main__":
    main()
