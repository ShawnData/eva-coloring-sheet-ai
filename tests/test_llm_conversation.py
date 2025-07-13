#!/usr/bin/env python3
"""
Test script for the enhanced voice assistant with LLM conversation capabilities
"""

import os
import pytest
from src.agents.voice_assistant import VoiceAssistantAgent

class TestLLMConversation:
    """Test class for LLM conversation capabilities"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Check if OpenAI API key is set
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY environment variable is not set")
        
        self.agent = VoiceAssistantAgent()
    
    def test_general_conversation(self):
        """Test the LLM conversation capabilities for general conversation"""
        test_inputs = [
            "Hello!",
            "How are you today?",
            "What's your favorite color?",
            "I love unicorns!",
            "Can you tell me a story?"
        ]
        
        for test_input in test_inputs:
            result = self.agent.process_voice_input(test_input)
            assert isinstance(result, dict)
            assert "message" in result
            assert result["message"] is not None
    
    def test_coloring_sheet_request(self):
        """Test the LLM conversation capabilities for coloring sheet requests"""
        result = self.agent.process_voice_input("I want a cat coloring sheet")
        assert isinstance(result, dict)
        assert "message" in result
        assert result["message"] is not None

def test_llm_conversation_integration():
    """Integration test for the LLM conversation capabilities"""
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY environment variable is not set")
    
    try:
        # Initialize the voice assistant
        agent = VoiceAssistantAgent()
        
        # Test general conversation (non-coloring sheet request)
        test_inputs = [
            "Hello!",
            "How are you today?",
            "What's your favorite color?",
            "I love unicorns!",
            "Can you tell me a story?"
        ]
        
        for test_input in test_inputs:
            result = agent.process_voice_input(test_input)
            assert isinstance(result, dict)
            assert "message" in result
        
        # Test coloring sheet request
        result = agent.process_voice_input("I want a cat coloring sheet")
        assert isinstance(result, dict)
        assert "message" in result
        
    except Exception as e:
        pytest.fail(f"Error during test: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__]) 