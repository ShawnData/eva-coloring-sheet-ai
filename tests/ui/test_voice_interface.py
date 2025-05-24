import pytest
from unittest.mock import Mock, patch
from src.ui.voice_interface import VoiceInterface

@pytest.fixture
def mock_voice_agent():
    """Fixture to create a mock VoiceAgent"""
    agent = Mock()
    agent.process_voice_input.return_value = "Test transcription"
    return agent

@pytest.fixture
def voice_interface(mock_voice_agent):
    """Fixture to create a VoiceInterface instance with mocked dependencies"""
    return VoiceInterface(mock_voice_agent)

def test_voice_interface_initialization(voice_interface, mock_voice_agent):
    """Test VoiceInterface initialization"""
    assert voice_interface.voice_agent == mock_voice_agent

def test_process_voice(voice_interface, mock_voice_agent):
    """Test voice processing through the interface"""
    result = voice_interface.process_voice()
    
    assert result == "Test transcription"
    mock_voice_agent.process_voice_input.assert_called_once()

def test_create_interface(voice_interface):
    """Test Gradio interface creation"""
    with patch('gradio.Interface') as mock_interface:
        interface = voice_interface.create_interface()
        
        # Verify interface creation with correct parameters
        mock_interface.assert_called_once_with(
            fn=voice_interface.process_voice,
            inputs=None,
            outputs="text",
            title="Eva's Coloring Sheet AI - Voice Input",
            description="Click the button below to start recording your voice input.",
            allow_flagging="never"
        )
        assert interface == mock_interface.return_value

def test_launch(voice_interface):
    """Test interface launching"""
    with patch.object(voice_interface, 'create_interface') as mock_create:
        mock_interface = Mock()
        mock_create.return_value = mock_interface
        
        voice_interface.launch()
        
        mock_create.assert_called_once()
        mock_interface.launch.assert_called_once()

def test_error_handling(voice_interface, mock_voice_agent):
    """Test error handling in voice processing"""
    mock_voice_agent.process_voice_input.side_effect = Exception("Processing failed")
    
    with pytest.raises(Exception) as exc_info:
        voice_interface.process_voice()
    
    assert str(exc_info.value) == "Processing failed" 