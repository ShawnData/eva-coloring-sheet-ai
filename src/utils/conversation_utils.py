"""
Conversation utilities for managing multi-turn conversations in the coloring sheet AI system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
import json
from datetime import datetime


@dataclass
class ConversationState:
    """Represents the state of a conversation session."""
    
    # Core conversation data
    requirements: Dict[str, Any] = field(default_factory=dict)
    keywords: List[str] = field(default_factory=list)  # NEW: List of keywords extracted from conversation
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    
    # Conversation flow state
    is_complete: bool = False
    is_confirmed: bool = False
    current_phase: str = "collecting"  # "collecting", "confirming", "generating"
    
    # Metadata
    session_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.last_updated = datetime.now()
    
    def update_requirements(self, new_requirements: Dict[str, Any]):
        """Update the collected requirements."""
        self.requirements.update(new_requirements)
        self.last_updated = datetime.now()
    
    def add_keywords(self, new_keywords: List[str]):
        """Add new keywords to the list, avoiding duplicates."""
        for keyword in new_keywords:
            if keyword.lower() not in [k.lower() for k in self.keywords]:
                self.keywords.append(keyword)
        self.last_updated = datetime.now()
    
    def get_keywords(self) -> List[str]:
        """Get the current list of keywords."""
        return self.keywords.copy()
    
    def set_phase(self, phase: str):
        """Set the current conversation phase."""
        valid_phases = ["collecting", "confirming", "generating", "complete"]
        if phase not in valid_phases:
            raise ValueError(f"Invalid phase: {phase}. Must be one of {valid_phases}")
        self.current_phase = phase
        self.last_updated = datetime.now()
    
    def mark_complete(self):
        """Mark requirements as complete."""
        self.is_complete = True
        self.last_updated = datetime.now()
    
    def mark_confirmed(self):
        """Mark requirements as confirmed by the child."""
        self.is_confirmed = True
        self.last_updated = datetime.now()
    
    def reset(self):
        """Reset the conversation state for a new session."""
        self.requirements.clear()
        self.keywords.clear()
        self.conversation_history.clear()
        self.is_complete = False
        self.is_confirmed = False
        self.current_phase = "collecting"
        self.last_updated = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert conversation state to dictionary for JSON serialization."""
        return {
            "requirements": self.requirements,
            "keywords": self.keywords,
            "conversation_history": self.conversation_history,
            "is_complete": self.is_complete,
            "is_confirmed": self.is_confirmed,
            "current_phase": self.current_phase,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationState':
        """Create conversation state from dictionary."""
        state = cls()
        state.requirements = data.get("requirements", {})
        state.keywords = data.get("keywords", [])
        state.conversation_history = data.get("conversation_history", [])
        state.is_complete = data.get("is_complete", False)
        state.is_confirmed = data.get("is_confirmed", False)
        state.current_phase = data.get("current_phase", "collecting")
        state.session_id = data.get("session_id")
        
        # Parse timestamps
        if "created_at" in data:
            state.created_at = datetime.fromisoformat(data["created_at"])
        if "last_updated" in data:
            state.last_updated = datetime.fromisoformat(data["last_updated"])
        
        return state


class ConversationManager:
    """Manages conversation sessions and state."""
    
    def __init__(self):
        self.sessions: Dict[str, ConversationState] = {}
    
    def create_session(self, session_id: str) -> ConversationState:
        """Create a new conversation session."""
        state = ConversationState(session_id=session_id)
        self.sessions[session_id] = state
        return state
    
    def get_session(self, session_id: str) -> Optional[ConversationState]:
        """Get an existing conversation session."""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, state: ConversationState):
        """Update a conversation session."""
        self.sessions[session_id] = state
    
    def delete_session(self, session_id: str):
        """Delete a conversation session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def reset_session(self, session_id: str) -> Optional[ConversationState]:
        """Reset a conversation session."""
        state = self.get_session(session_id)
        if state:
            state.reset()
            return state
        return None
