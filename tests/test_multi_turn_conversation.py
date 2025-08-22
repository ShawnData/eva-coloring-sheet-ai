"""
Tests for multi-turn conversation functionality
"""

import pytest
import json
from src.utils.conversation_utils import ConversationState, ConversationManager, extract_requirements_from_text, generate_prompt_from_requirements
from src.crews.coloring_sheet_crew import create_coloring_sheet_crew, process_conversation_turn


class TestConversationState:
    """Test conversation state management"""
    
    def test_conversation_state_creation(self):
        """Test creating a new conversation state"""
        state = ConversationState()
        assert state.is_complete == False
        assert state.is_confirmed == False
        assert state.current_phase == "collecting"
        assert len(state.conversation_history) == 0
        assert len(state.requirements) == 0
    
    def test_add_message(self):
        """Test adding messages to conversation history"""
        state = ConversationState()
        state.add_message("user", "I want a cat")
        state.add_message("assistant", "What kind of cat?")
        
        assert len(state.conversation_history) == 2
        assert state.conversation_history[0]["role"] == "user"
        assert state.conversation_history[0]["content"] == "I want a cat"
        assert state.conversation_history[1]["role"] == "assistant"
        assert state.conversation_history[1]["content"] == "What kind of cat?"
    
    def test_update_requirements(self):
        """Test updating requirements"""
        state = ConversationState()
        state.update_requirements({"subject": "cat", "color": "orange"})
        
        assert state.requirements["subject"] == "cat"
        assert state.requirements["color"] == "orange"
    
    def test_phase_transitions(self):
        """Test conversation phase transitions"""
        state = ConversationState()
        assert state.current_phase == "collecting"
        
        state.set_phase("confirming")
        assert state.current_phase == "confirming"
        
        state.set_phase("generating")
        assert state.current_phase == "generating"
        
        state.set_phase("complete")
        assert state.current_phase == "complete"
    
    def test_invalid_phase(self):
        """Test that invalid phases raise an error"""
        state = ConversationState()
        with pytest.raises(ValueError):
            state.set_phase("invalid_phase")
    
    def test_serialization(self):
        """Test conversation state serialization"""
        state = ConversationState()
        state.add_message("user", "I want a cat")
        state.update_requirements({"subject": "cat"})
        state.set_phase("confirming")
        
        # Convert to dict
        state_dict = state.to_dict()
        assert "requirements" in state_dict
        assert "conversation_history" in state_dict
        assert "current_phase" in state_dict
        
        # Convert back from dict
        new_state = ConversationState.from_dict(state_dict)
        assert new_state.requirements == state.requirements
        assert new_state.current_phase == state.current_phase
        assert len(new_state.conversation_history) == len(state.conversation_history)


class TestConversationManager:
    """Test conversation manager functionality"""
    
    def test_create_session(self):
        """Test creating a new conversation session"""
        manager = ConversationManager()
        session_id = "test_session"
        state = manager.create_session(session_id)
        
        assert state.session_id == session_id
        assert manager.get_session(session_id) == state
    
    def test_get_nonexistent_session(self):
        """Test getting a session that doesn't exist"""
        manager = ConversationManager()
        assert manager.get_session("nonexistent") is None
    
    def test_reset_session(self):
        """Test resetting a conversation session"""
        manager = ConversationManager()
        session_id = "test_session"
        state = manager.create_session(session_id)
        
        # Add some data
        state.add_message("user", "I want a cat")
        state.update_requirements({"subject": "cat"})
        
        # Reset the session
        reset_state = manager.reset_session(session_id)
        assert reset_state is not None
        assert len(reset_state.conversation_history) == 0
        assert len(reset_state.requirements) == 0
        assert reset_state.current_phase == "collecting"
    
    def test_delete_session(self):
        """Test deleting a conversation session"""
        manager = ConversationManager()
        session_id = "test_session"
        manager.create_session(session_id)
        
        assert manager.get_session(session_id) is not None
        manager.delete_session(session_id)
        assert manager.get_session(session_id) is None


class TestRequirementsExtraction:
    """Test requirements extraction from text"""
    
    def test_extract_subject(self):
        """Test extracting subject from text"""
        text = "I want a cat coloring sheet"
        requirements = extract_requirements_from_text(text)
        assert requirements["subject"] == "cat"
    
    def test_extract_colors(self):
        """Test extracting colors from text"""
        text = "I want an orange cat"
        requirements = extract_requirements_from_text(text)
        assert "orange" in requirements["colors"]
    
    def test_extract_actions(self):
        """Test extracting actions from text"""
        text = "A cat playing with a ball"
        requirements = extract_requirements_from_text(text)
        assert requirements["action"] == "playing"
    
    def test_extract_objects(self):
        """Test extracting objects from text"""
        text = "A cat with a ball"
        requirements = extract_requirements_from_text(text)
        assert "ball" in requirements["objects"]
    
    def test_no_requirements(self):
        """Test text with no extractable requirements"""
        text = "Hello, how are you?"
        requirements = extract_requirements_from_text(text)
        assert len(requirements) == 0


class TestPromptGeneration:
    """Test prompt generation from requirements"""
    
    def test_basic_prompt_generation(self):
        """Test generating a basic prompt"""
        requirements = {
            "subject": "cat",
            "action": "playing",
            "colors": ["orange"],
            "objects": ["ball"]
        }
        
        prompt = generate_prompt_from_requirements(requirements)
        assert "cat" in prompt
        assert "playing" in prompt
        assert "orange" in prompt
        assert "ball" in prompt
        assert "coloring sheet" in prompt
    
    def test_minimal_requirements(self):
        """Test prompt generation with minimal requirements"""
        requirements = {"subject": "dog"}
        prompt = generate_prompt_from_requirements(requirements)
        assert "dog" in prompt
        assert "coloring sheet" in prompt
    
    def test_empty_requirements(self):
        """Test prompt generation with empty requirements"""
        requirements = {}
        prompt = generate_prompt_from_requirements(requirements)
        assert "coloring sheet" in prompt


class TestConversationTurn:
    """Test conversation turn processing"""
    
    def test_first_conversation_turn(self):
        """Test processing the first turn in a conversation"""
        crew = create_coloring_sheet_crew()
        result = process_conversation_turn(crew, "I want a cat")
        
        assert "message" in result
        assert "conversation_state" in result
        assert "should_generate_image" in result
        assert result["should_generate_image"] == False  # Should not generate image on first turn
        assert result["conversation_state"] is not None
    
    def test_conversation_with_state(self):
        """Test processing a conversation turn with existing state"""
        crew = create_coloring_sheet_crew()
        state = ConversationState()
        state.add_message("user", "I want a cat")
        state.add_message("assistant", "What kind of cat?")
        state.update_requirements({"subject": "cat"})
        
        result = process_conversation_turn(crew, "A house cat", state)
        
        assert "message" in result
        assert "conversation_state" in result
        assert result["conversation_state"] is not None


if __name__ == "__main__":
    pytest.main([__file__]) 