#!/usr/bin/env python3
"""
Test script for conversation keyword extraction and requirements collection
"""

import pytest
from src.utils.conversation_utils import (
    ConversationState, 
    extract_requirements_from_text, 
    generate_prompt_from_requirements
)


class TestConversationKeywords:
    """Test class for conversation keyword extraction and management"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.conversation_state = ConversationState()
    
    def test_keyword_extraction_basic(self):
        """Test basic keyword extraction from text"""
        text = "I want a cat coloring sheet"
        requirements, keywords = extract_requirements_from_text(text)
        
        assert requirements["subject"] == "cat"
        assert "cat" in keywords
        assert len(keywords) >= 1
    
    def test_keyword_extraction_with_descriptions(self):
        """Test keyword extraction with descriptive words"""
        text = "I want a cute cat with rainbow"
        requirements, keywords = extract_requirements_from_text(text)
        
        assert requirements["subject"] == "cat"
        assert "cute" in keywords
        assert "rainbow" in keywords
        assert "cat" in keywords
        assert len(keywords) >= 3
    
    def test_keyword_extraction_with_actions(self):
        """Test keyword extraction with action words"""
        text = "A cat playing with a ball"
        requirements, keywords = extract_requirements_from_text(text)
        
        assert requirements["subject"] == "cat"
        assert requirements["action"] == "playing"
        assert "cat" in keywords
        assert "playing" in keywords
        assert "ball" in keywords
    
    def test_keyword_extraction_with_colors(self):
        """Test keyword extraction with color words"""
        text = "An orange cat with blue eyes"
        requirements, keywords = extract_requirements_from_text(text)
        
        assert requirements["subject"] == "cat"
        assert "orange" in requirements["colors"]
        assert "blue" in requirements["colors"]
        assert "cat" in keywords
        assert "orange" in keywords
        assert "blue" in keywords
    
    def test_conversation_state_keywords(self):
        """Test conversation state keyword management"""
        # Add keywords
        self.conversation_state.add_keywords(["cat", "cute"])
        assert "cat" in self.conversation_state.keywords
        assert "cute" in self.conversation_state.keywords
        
        # Add more keywords (should avoid duplicates)
        self.conversation_state.add_keywords(["cat", "rainbow"])
        assert len(self.conversation_state.keywords) == 3  # cat, cute, rainbow
        assert "rainbow" in self.conversation_state.keywords
        
        # Test case-insensitive duplicate detection
        self.conversation_state.add_keywords(["CAT", "CUTE"])
        assert len(self.conversation_state.keywords) == 3  # Should not add duplicates
    
    def test_conversation_state_serialization(self):
        """Test conversation state serialization with keywords"""
        self.conversation_state.add_keywords(["cat", "cute", "rainbow"])
        self.conversation_state.update_requirements({"subject": "cat"})
        
        # Convert to dict and back
        state_dict = self.conversation_state.to_dict()
        new_state = ConversationState.from_dict(state_dict)
        
        assert new_state.keywords == ["cat", "cute", "rainbow"]
        assert new_state.requirements["subject"] == "cat"
    
    def test_prompt_generation_with_keywords(self):
        """Test prompt generation using both requirements and keywords"""
        requirements = {
            "subject": "cat",
            "description": "cute",
            "colors": ["orange"],
            "objects": ["ball"]
        }
        keywords = ["cat", "cute", "orange", "ball", "playing", "friendly"]
        
        prompt = generate_prompt_from_requirements(requirements, keywords)
        
        # Should include all the basic requirements
        assert "cat" in prompt
        assert "cute" in prompt
        assert "orange" in prompt
        assert "ball" in prompt
        
        # Should include additional keywords not in requirements
        assert "playing" in prompt
        assert "friendly" in prompt
        
        # Should include coloring sheet specifications
        assert "coloring sheet" in prompt
        assert "black and white" in prompt
    
    def test_prompt_generation_without_keywords(self):
        """Test prompt generation with only requirements (backward compatibility)"""
        requirements = {
            "subject": "cat",
            "description": "cute",
            "colors": ["orange"]
        }
        
        prompt = generate_prompt_from_requirements(requirements)
        
        assert "cat" in prompt
        assert "cute" in prompt
        assert "orange" in prompt
        assert "coloring sheet" in prompt
    
    def test_complex_conversation_flow(self):
        """Test a complex conversation flow with multiple turns"""
        # Turn 1: Initial request
        text1 = "I want a cat coloring sheet"
        req1, kw1 = extract_requirements_from_text(text1)
        self.conversation_state.update_requirements(req1)
        self.conversation_state.add_keywords(kw1)
        
        assert self.conversation_state.requirements["subject"] == "cat"
        assert "cat" in self.conversation_state.keywords
        
        # Turn 2: Add description
        text2 = "A cute cat"
        req2, kw2 = extract_requirements_from_text(text2)
        self.conversation_state.update_requirements(req2)
        self.conversation_state.add_keywords(kw2)
        
        assert "cute" in self.conversation_state.keywords
        assert len(self.conversation_state.keywords) >= 2
        
        # Turn 3: Add action and object
        text3 = "Playing with a rainbow"
        req3, kw3 = extract_requirements_from_text(text3)
        self.conversation_state.update_requirements(req3)
        self.conversation_state.add_keywords(kw3)
        
        assert "playing" in self.conversation_state.keywords
        assert "rainbow" in self.conversation_state.keywords
        
        # Final state should have all keywords
        final_keywords = self.conversation_state.get_keywords()
        assert "cat" in final_keywords
        assert "cute" in final_keywords
        assert "playing" in final_keywords
        assert "rainbow" in final_keywords
    
    def test_keyword_deduplication(self):
        """Test that keywords are properly deduplicated"""
        # Add same keywords multiple times
        self.conversation_state.add_keywords(["cat", "cute"])
        self.conversation_state.add_keywords(["cat", "rainbow"])
        self.conversation_state.add_keywords(["cute", "playing"])
        
        keywords = self.conversation_state.get_keywords()
        assert len(keywords) == 4  # cat, cute, rainbow, playing
        assert keywords.count("cat") == 1
        assert keywords.count("cute") == 1
    
    def test_reset_conversation_state(self):
        """Test that conversation state reset clears keywords"""
        self.conversation_state.add_keywords(["cat", "cute", "rainbow"])
        self.conversation_state.update_requirements({"subject": "cat"})
        
        assert len(self.conversation_state.keywords) > 0
        assert len(self.conversation_state.requirements) > 0
        
        self.conversation_state.reset()
        
        assert len(self.conversation_state.keywords) == 0
        assert len(self.conversation_state.requirements) == 0


def test_keyword_extraction_edge_cases():
    """Test edge cases in keyword extraction"""
    
    # Test empty input
    requirements, keywords = extract_requirements_from_text("")
    assert len(requirements) == 0
    assert len(keywords) == 0
    
    # Test input with no recognizable keywords
    requirements, keywords = extract_requirements_from_text("Hello there!")
    assert len(requirements) == 0
    assert len(keywords) == 0
    
    # Test input with numbers
    requirements, keywords = extract_requirements_from_text("I want 3 cats")
    assert "3" in keywords
    
    # Test input with special keywords
    requirements, keywords = extract_requirements_from_text("A magical unicorn in a forest")
    assert "unicorn" in keywords
    assert "magical" in keywords
    assert "forest" in keywords


if __name__ == "__main__":
    pytest.main([__file__]) 