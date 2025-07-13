import pytest
from src.agents.conversation_summarizer import ConversationSummarizerAgent

class TestConversationSummarizerAgent:
    
    def setup_method(self):
        """Set up test fixtures"""
        self.summarizer = ConversationSummarizerAgent()
    
    def test_clean_transcription(self):
        """Test transcription cleaning functionality"""
        # Test basic cleaning
        result = self.summarizer._clean_transcription("Um, I want a cat, you know")
        assert "um" not in result
        assert "you know" not in result
        assert "cat" in result
        
        # Test whitespace normalization
        result = self.summarizer._clean_transcription("  I   want   a   cat  ")
        assert result == "i want a cat"
    
    def test_is_coloring_sheet_request(self):
        """Test detection of coloring sheet requests"""
        # Valid requests
        assert self.summarizer._is_coloring_sheet_request("i want a cat coloring sheet")
        assert self.summarizer._is_coloring_sheet_request("make me a dog picture")
        assert self.summarizer._is_coloring_sheet_request("create a flower drawing")
        assert self.summarizer._is_coloring_sheet_request("show me a car")
        
        # Invalid requests
        assert not self.summarizer._is_coloring_sheet_request("hello how are you")
        assert not self.summarizer._is_coloring_sheet_request("what's the weather")
    
    def test_extract_subject(self):
        """Test subject extraction from requests"""
        # Test various patterns
        assert self.summarizer._extract_subject("i want a cat") == "cat"
        assert self.summarizer._extract_subject("make me a dog picture") == "dog picture"
        assert self.summarizer._extract_subject("coloring sheet of a flower") == "flower"
        assert self.summarizer._extract_subject("draw a car please") == "car"
        
        # Test fallback for short inputs
        assert self.summarizer._extract_subject("cat") == "cat"
    
    def test_contains_inappropriate_content(self):
        """Test inappropriate content filtering"""
        # Test inappropriate content
        assert self.summarizer._contains_inappropriate_content("scary monster")
        assert self.summarizer._contains_inappropriate_content("gun weapon")
        assert self.summarizer._contains_inappropriate_content("adult content")
        
        # Test appropriate content
        assert not self.summarizer._contains_inappropriate_content("friendly cat")
        assert not self.summarizer._contains_inappropriate_content("happy dog")
        assert not self.summarizer._contains_inappropriate_content("beautiful flower")
    
    def test_create_structured_prompt(self):
        """Test structured prompt creation"""
        # Test with modifiers
        result = self.summarizer._create_structured_prompt("cat", "i want a cute cat")
        assert "cute" in result
        
        result = self.summarizer._create_structured_prompt("dog", "make a big dog")
        assert "big" in result
        
        # Test default case
        result = self.summarizer._create_structured_prompt("flower", "i want a flower")
        assert "friendly" in result
    
    def test_summarize_conversation_coloring_request(self):
        """Test full conversation summarization for coloring requests"""
        result = self.summarizer.summarize_conversation("I want a cat coloring sheet")
        
        assert result["is_coloring_request"] is True
        assert "cat" in result["prompt"]
        assert result["confidence"] > 0.0
        assert "message" in result
    
    def test_summarize_conversation_non_coloring_request(self):
        """Test conversation summarization for non-coloring requests"""
        result = self.summarizer.summarize_conversation("Hello, how are you?")
        
        assert result["is_coloring_request"] is False
        assert result["prompt"] is None
        assert result["confidence"] == 0.0
        assert "message" in result
    
    def test_summarize_conversation_inappropriate_content(self):
        """Test handling of inappropriate content"""
        result = self.summarizer.summarize_conversation("I want a scary monster")
        
        assert result["is_coloring_request"] is True
        assert "friendly" in result["prompt"] or "animal" in result["prompt"]
        assert result["confidence"] > 0.0
        assert "message" in result
    
    def test_calculate_confidence(self):
        """Test confidence calculation"""
        # High confidence cases
        assert self.summarizer._calculate_confidence("i want a cat coloring sheet") > 0.8
        
        # Lower confidence cases
        assert self.summarizer._calculate_confidence("maybe a cat") < 0.8
        assert self.summarizer._calculate_confidence("cat") < 0.8  # Too short 