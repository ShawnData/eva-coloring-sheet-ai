#!/usr/bin/env python3
"""
Test script to verify voice processing components
"""

import os
import pytest
from src.crews.coloring_sheet_crew import ColoringSheetCrew
from src.ui.interface import ColoringSheetInterface

class TestVoiceProcessing:
    """Test class for voice processing components"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Set a test API key if not present
        if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = "test-key"
    
    def test_crew_initialization(self):
        """Test that the crew can be initialized"""
        try:
            crew = ColoringSheetCrew()
            assert crew is not None
        except Exception as e:
            pytest.fail(f"Crew initialization failed: {e}")
    
    def test_voice_processing(self):
        """Test voice processing with mock data"""
        crew = ColoringSheetCrew()
        
        # Test with various inputs
        test_inputs = [
            "I want a cat coloring sheet",
            "Hello, how are you?",
            "Make me a dog picture"
        ]
        
        for test_input in test_inputs:
            try:
                result = crew.process_voice_input(test_input)
                assert isinstance(result, dict)
                assert "message" in result
            except Exception as e:
                pytest.fail(f"Error processing '{test_input}': {e}")
    
    def test_interface_initialization(self):
        """Test that the interface can be initialized"""
        try:
            crew = ColoringSheetCrew()
            interface = ColoringSheetInterface(crew)
            assert interface is not None
        except Exception as e:
            pytest.fail(f"Interface initialization failed: {e}")
    
    def test_audio_utils(self):
        """Test audio utilities"""
        try:
            from src.utils.audio_utils import AudioUtils
            audio_utils = AudioUtils()
            assert audio_utils is not None
            
            # Test TTS generation
            test_message = "Hello, this is a test message."
            tts_file = audio_utils.generate_tts(test_message)
            assert tts_file is not None
            
        except Exception as e:
            pytest.fail(f"Audio utilities test failed: {e}")

def test_voice_processing_integration():
    """Integration test for voice processing"""
    # Set a test API key if not present
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "test-key"
    
    try:
        crew = ColoringSheetCrew()
        interface = ColoringSheetInterface(crew)
        
        # Test basic functionality
        result = crew.process_voice_input("I want a cat coloring sheet")
        assert isinstance(result, dict)
        assert "message" in result
        
    except Exception as e:
        pytest.fail(f"Integration test failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__]) 