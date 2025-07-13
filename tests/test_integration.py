import os
import sys
from unittest.mock import Mock, patch
from src.crews.coloring_sheet_crew import ColoringSheetCrew

class TestIntegration:
    
    def setup_method(self):
        """Set up test fixtures"""
        # Mock environment variables
        os.environ['OPENAI_API_KEY'] = 'test-key'
        self.crew = ColoringSheetCrew()
    
    def test_process_voice_input_coloring_request(self):
        """Test complete workflow for coloring sheet request"""
        # Test with a valid coloring request
        result = self.crew.process_voice_input("I want a cat coloring sheet")
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "message" in result
        assert "image_url" in result
        
        # Verify it's a coloring request
        assert "cat" in result["message"].lower() or "coloring" in result["message"].lower()
    
    def test_process_voice_input_non_coloring_request(self):
        """Test workflow for non-coloring requests"""
        # Test with a general conversation
        result = self.crew.process_voice_input("Hello, how are you?")
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "message" in result
        assert "image_url" in result
        
        # Verify no image URL for non-coloring requests
        assert result["image_url"] is None
    
    def test_process_voice_input_inappropriate_content(self):
        """Test workflow with inappropriate content"""
        # Test with inappropriate content
        result = self.crew.process_voice_input("I want a scary monster")
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "message" in result
        assert "image_url" in result
        
        # Should provide a safe alternative
        assert "friendly" in result["message"].lower() or "animal" in result["message"].lower()
    
    def test_process_voice_input_empty_input(self):
        """Test workflow with empty input"""
        result = self.crew.process_voice_input("")
        
        # Should handle gracefully
        assert isinstance(result, dict)
        assert "message" in result
    
    def test_process_voice_input_error_handling(self):
        """Test error handling in the workflow"""
        # Mock the summarizer to raise an exception
        with patch.object(self.crew.summarizer_agent, 'summarize_conversation') as mock_summarize:
            mock_summarize.side_effect = Exception("Test error")
            
            result = self.crew.process_voice_input("I want a cat")
            
            # Should handle error gracefully
            assert isinstance(result, dict)
            assert "message" in result
            assert "error" in result 