import pytest
import os
import numpy as np
from unittest.mock import Mock, patch, mock_open
from src.agents.voice_agent import VoiceAgent

@pytest.fixture
def mock_openai_client():
    """Fixture to mock OpenAI client"""
    with patch('openai.OpenAI') as mock_client:
        mock_instance = Mock()
        mock_instance.audio.transcriptions.create.return_value.text = "Test transcription"
        mock_client.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_sounddevice():
    """Fixture to mock sounddevice"""
    with patch('sounddevice.rec') as mock_rec, \
         patch('sounddevice.wait') as mock_wait:
        mock_rec.return_value = np.zeros((44100, 1))  # 1 second of silence
        yield mock_rec, mock_wait

@pytest.fixture
def voice_agent(mock_openai_client):
    """Fixture to create a VoiceAgent instance with mocked dependencies"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
        agent = VoiceAgent()
        return agent

def test_voice_agent_initialization(voice_agent):
    """Test VoiceAgent initialization"""
    assert voice_agent.sample_rate == 44100
    assert voice_agent.channels == 1
    assert voice_agent.duration == 5
    assert voice_agent.agent is not None

def test_record_audio(voice_agent, mock_sounddevice):
    """Test audio recording functionality"""
    mock_rec, mock_wait = mock_sounddevice
    recording = voice_agent.record_audio()
    
    # Verify recording parameters
    mock_rec.assert_called_once_with(
        int(voice_agent.duration * voice_agent.sample_rate),
        samplerate=voice_agent.sample_rate,
        channels=voice_agent.channels
    )
    mock_wait.assert_called_once()
    assert isinstance(recording, np.ndarray)

def test_save_audio(voice_agent):
    """Test audio saving functionality"""
    test_recording = np.zeros((44100, 1))
    test_filename = "test_recording.wav"
    
    with patch('src.agents.voice_agent.write') as mock_write:
        voice_agent.save_audio(test_recording, test_filename)
        mock_write.assert_called_once_with(
            test_filename,
            voice_agent.sample_rate,
            test_recording
        )

def test_transcribe_audio(voice_agent, mock_openai_client):
    """Test audio transcription functionality"""
    test_file = "test.wav"
    
    # Create a mock file
    mock_file_content = b"mock audio data"
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        transcription = voice_agent.transcribe_audio(test_file)
        
        assert transcription == "Test transcription"
        mock_openai_client.audio.transcriptions.create.assert_called_once()

def test_process_voice_input(voice_agent, mock_sounddevice, mock_openai_client):
    """Test complete voice input processing"""
    with patch('os.remove') as mock_remove:
        transcription = voice_agent.process_voice_input()
        
        # Verify the complete flow
        assert transcription == "Test transcription"
        mock_remove.assert_called_once()  # Verify cleanup

def test_process_voice_input_error_handling(voice_agent):
    """Test error handling in voice input processing"""
    with patch.object(voice_agent, 'record_audio', side_effect=Exception("Recording failed")):
        with pytest.raises(Exception) as exc_info:
            voice_agent.process_voice_input()
        assert str(exc_info.value) == "Recording failed" 