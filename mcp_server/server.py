from fastmcp import FastMCP
from mcp_server.utils.audio_utils import AudioUtils

# Create a server instance
mcp = FastMCP(name="voice-assistant")
audio_utils = AudioUtils()


@mcp.tool()
def speak(text: str):
    audio_file = audio_utils.generate_tts(text)
    audio_utils.play_audio(audio_file)
