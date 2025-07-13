#!/usr/bin/env python3
"""
Test script to verify core functionality of the coloring sheet AI
"""

import os
import pytest
from dotenv import load_dotenv
from src.crews.coloring_sheet_crew import ColoringSheetCrew

class TestCoreFunctionality:
    """Test class for core functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        load_dotenv()
        
        # Check if OpenAI API key is set
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY environment variable is not set")
        
        self.crew = ColoringSheetCrew()
    
    def test_voice_processing_coloring_request(self):
        """Test voice processing for coloring sheet requests"""
        test_cases = [
            "I want a cat coloring sheet",
            "Can you make me a dog picture to color?",
        ]
        
        for test_input in test_cases:
            result = self.crew.process_voice_input(test_input)
            assert isinstance(result, dict)
            assert "message" in result
            assert "image_url" in result
    
    def test_voice_processing_conversation(self):
        """Test voice processing for general conversation"""
        test_cases = [
            "Hello",
            "What's the weather like?"
        ]
        
        for test_input in test_cases:
            result = self.crew.process_voice_input(test_input)
            assert isinstance(result, dict)
            assert "message" in result
            assert "image_url" in result
            # For conversation, image_url should be None
            assert result["image_url"] is None

def test_voice_processing_integration():
    """Integration test for voice processing functionality"""
    load_dotenv()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY environment variable is not set")
    
    # Create the crew
    try:
        crew = ColoringSheetCrew()
    except Exception as e:
        pytest.fail(f"Failed to create crew: {e}")
    
    # Test cases
    test_cases = [
        "I want a cat coloring sheet",
        "Hello",
        "Can you make me a dog picture to color?",
        "What's the weather like?"
    ]
    
    for test_input in test_cases:
        try:
            result = crew.process_voice_input(test_input)
            assert isinstance(result, dict)
            assert "message" in result
            assert "image_url" in result
            
        except Exception as e:
            pytest.fail(f"Processing failed for '{test_input}': {e}")

if __name__ == "__main__":
    pytest.main([__file__]) 