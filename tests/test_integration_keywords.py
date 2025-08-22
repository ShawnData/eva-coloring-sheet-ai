#!/usr/bin/env python3
"""
Integration test for the conversation requirements collection with keywords
"""

import pytest
import json
from src.utils.conversation_utils import ConversationState, extract_requirements_from_text


class TestIntegrationKeywords:
    """Integration test class for keyword collection system"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.conversation_state = ConversationState()
    
    def test_conversation_state_persistence(self):
        """Test that conversation state persists keywords across turns"""
        # First turn
        voice_input1 = "I want a cat"
        requirements1, keywords1 = extract_requirements_from_text(voice_input1)
        self.conversation_state.update_requirements(requirements1)
        self.conversation_state.add_keywords(keywords1)
        
        # Second turn
        voice_input2 = "A cute cat"
        requirements2, keywords2 = extract_requirements_from_text(voice_input2)
        self.conversation_state.update_requirements(requirements2)
        self.conversation_state.add_keywords(keywords2)
        
        # Third turn
        voice_input3 = "Playing with a ball"
        requirements3, keywords3 = extract_requirements_from_text(voice_input3)
        self.conversation_state.update_requirements(requirements3)
        self.conversation_state.add_keywords(keywords3)
        
        # Verify all keywords are present
        final_keywords = self.conversation_state.get_keywords()
        assert "cat" in final_keywords
        assert "cute" in final_keywords
        assert "playing" in final_keywords
        assert "ball" in final_keywords
        assert len(final_keywords) >= 4
    
    def test_conversation_state_serialization(self):
        """Test that conversation state with keywords can be serialized"""
        # Add some data
        self.conversation_state.add_keywords(["cat", "cute", "rainbow"])
        self.conversation_state.update_requirements({"subject": "cat"})
        self.conversation_state.add_message("user", "I want a cat")
        self.conversation_state.add_message("assistant", "Great! What kind of cat?")
        
        # Serialize to JSON
        state_dict = self.conversation_state.to_dict()
        state_json = json.dumps(state_dict)
        
        # Deserialize
        parsed_dict = json.loads(state_json)
        new_state = ConversationState.from_dict(parsed_dict)
        
        # Verify data is preserved
        assert new_state.keywords == ["cat", "cute", "rainbow"]
        assert new_state.requirements["subject"] == "cat"
        assert len(new_state.conversation_history) == 2
    
    def test_keyword_deduplication_integration(self):
        """Test keyword deduplication in a real conversation flow"""
        # Simulate multiple turns with overlapping keywords
        turns = [
            "I want a cat",
            "A cute cat",
            "The cat is cute",
            "Playing with a ball",
            "The cat is playing"
        ]
        
        for turn in turns:
            requirements, keywords = extract_requirements_from_text(turn)
            self.conversation_state.update_requirements(requirements)
            self.conversation_state.add_keywords(keywords)
        
        # Verify no duplicates
        final_keywords = self.conversation_state.get_keywords()
        assert final_keywords.count("cat") == 1
        assert final_keywords.count("cute") == 1
        assert final_keywords.count("playing") == 1
        assert "ball" in final_keywords
    
    def test_conversation_completion_with_keywords(self):
        """Test that conversation completion includes all keywords"""
        # Build up a conversation
        self.conversation_state.add_keywords(["cat", "cute", "rainbow", "playing"])
        self.conversation_state.update_requirements({
            "subject": "cat",
            "description": "cute",
            "action": "playing",
            "objects": ["rainbow"]
        })
        
        # Mark as complete
        self.conversation_state.mark_complete()
        self.conversation_state.mark_confirmed()
        
        # Verify state
        assert self.conversation_state.is_complete
        assert self.conversation_state.is_confirmed
        assert len(self.conversation_state.get_keywords()) == 4
        
        # Verify serialization preserves completion state
        state_dict = self.conversation_state.to_dict()
        new_state = ConversationState.from_dict(state_dict)
        assert new_state.is_complete
        assert new_state.is_confirmed
        assert len(new_state.get_keywords()) == 4
    
    def test_keyword_extraction_complex_scenario(self):
        """Test complex keyword extraction scenario"""
        # Complex input with multiple elements
        complex_input = "I want a magical unicorn playing in a rainbow forest with three tiny butterflies"
        requirements, keywords = extract_requirements_from_text(complex_input)
        
        # Verify requirements
        assert requirements["subject"] == "unicorn"
        assert requirements["action"] == "playing"
        assert "rainbow" in requirements["colors"]
        
        # Verify keywords (based on actual extraction)
        assert "unicorn" in keywords
        assert "magical" in keywords
        assert "playing" in keywords
        assert "rainbow" in keywords
        assert "forest" in keywords
        assert "tiny" in keywords
        assert "magic" in keywords  # "magical" also adds "magic"
        
        # Add to conversation state
        self.conversation_state.update_requirements(requirements)
        self.conversation_state.add_keywords(keywords)
        
        # Verify state
        final_keywords = self.conversation_state.get_keywords()
        assert len(final_keywords) >= 7  # Should have multiple keywords


def test_keyword_extraction_performance():
    """Test that keyword extraction is performant"""
    import time
    
    # Test with various inputs
    test_inputs = [
        "I want a cat",
        "A cute cat playing with a ball",
        "A magical unicorn in a forest with rainbow",
        "Three tiny blue birds flying in the sky",
        "A friendly robot wearing a hat and glasses"
    ]
    
    start_time = time.time()
    
    for input_text in test_inputs:
        requirements, keywords = extract_requirements_from_text(input_text)
        assert len(keywords) > 0
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Should process all inputs quickly (less than 1 second)
    assert processing_time < 1.0
    print(f"Processed {len(test_inputs)} inputs in {processing_time:.3f} seconds")


if __name__ == "__main__":
    pytest.main([__file__]) 