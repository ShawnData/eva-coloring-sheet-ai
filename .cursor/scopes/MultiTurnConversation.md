# Spec: Multi-Turn Conversation Enhancement for Voice Agent

## Purpose & User Problem
Currently, the voice agent processes each voice input independently and immediately generates a coloring sheet image. This creates a poor user experience where children cannot refine their requests or provide additional details through natural conversation. The system needs to support multi-turn conversations where the voice agent can collect all requirements and confirm with the child before proceeding to image generation.

## Success Criteria
- Voice agent can have multiple back-and-forth interactions with the child
- Agent collects all coloring sheet requirements through natural conversation
- Agent asks clarifying questions when needed (e.g., "What color should the cat be?", "Do you want it to be sitting or standing?")
- Agent confirms final requirements with the child before generating the image
- Child can modify or add details during the conversation
- Designer agent only generates image after voice agent confirms all requirements are complete
- Conversation state is maintained throughout the session
- Frontend supports ongoing conversation display

## Scope & Constraints

### In Scope
- Modify CrewAI structure to support conversation state management
- Update voice agent to handle multi-turn interactions
- Add conversation state tracking (requirements collected, confirmation status)
- Update API to support conversation sessions
- Modify frontend to display ongoing conversation
- Add conversation completion logic
- Support conversation reset/restart functionality

### Out of Scope
- Persistent conversation storage across sessions
- Multiple concurrent conversations
- Advanced conversation analytics
- Voice agent memory beyond current session

## Technical Considerations

### Conversation State Management
- Track collected requirements in a structured format
- Maintain conversation history within the session
- Track whether requirements are complete and confirmed
- Handle conversation flow states (collecting, confirming, generating)

### CrewAI Modifications
- Modify task structure to support iterative requirements collection
- Add conversation state to task inputs/outputs
- Implement conditional task execution based on conversation state
- Support task delegation for complex conversation flows

### API Changes
- Add conversation session management
- Support conversation state in request/response
- Handle conversation completion triggers
- Provide conversation reset endpoints

### Frontend Updates
- Display conversation history with user/assistant messages
- Show current conversation state (collecting requirements, confirming, generating)
- Add conversation controls (reset, continue, generate image)
- Support real-time conversation updates

## Conversation Flow Design

### Phase 1: Requirements Collection
```
Child: "I want a cat coloring sheet"
Agent: "Great! I'd love to help you create a cat coloring sheet. What kind of cat would you like? A big cat like a lion or a small cat like a house cat?"

Child: "A house cat"
Agent: "Perfect! A house cat it is. What should the cat be doing? Should it be sitting, sleeping, or playing?"

Child: "Playing with a ball"
Agent: "That sounds fun! A house cat playing with a ball. What color should the cat be?"

Child: "Orange"
Agent: "An orange house cat playing with a ball - that's going to be great! Is there anything else you'd like to add to your coloring sheet?"
```

### Phase 2: Confirmation
```
Agent: "Let me make sure I have everything right. You want a coloring sheet of an orange house cat playing with a ball. Is that correct?"

Child: "Yes"
Agent: "Perfect! I'll create your orange cat playing with a ball coloring sheet now. This might take a moment..."
```

### Phase 3: Image Generation
- Designer agent receives complete, confirmed requirements
- Generates image based on final prompt
- Returns image to child

## Implementation Plan

### Step 1: Conversation State Structure
```python
class ConversationState:
    requirements: dict  # Collected requirements
    conversation_history: list  # Message history
    is_complete: bool  # Whether requirements are complete
    is_confirmed: bool  # Whether child confirmed requirements
    current_phase: str  # "collecting", "confirming", "generating"
```

### Step 2: Modified Voice Agent Task
- Accept conversation state as input
- Update requirements based on new voice input
- Determine if more information is needed
- Return updated conversation state and response message

### Step 3: Conditional Task Execution
- Only execute designer task when requirements are complete and confirmed
- Support conversation continuation when more information is needed

### Step 4: API Session Management
- Track conversation sessions
- Maintain conversation state across requests
- Handle conversation completion and reset

## File Structure Changes
```
src/
├── crews/
│   ├── coloring_sheet_crew.py (modified for multi-turn)
│   └── conversation_state.py (new)
├── utils/
│   └── conversation_utils.py (new)
└── api_server.py (modified for sessions)
```

## Testing Strategy
- Unit tests for conversation state management
- Integration tests for multi-turn conversation flow
- Frontend tests for conversation UI
- End-to-end tests for complete conversation scenarios

## Success Metrics
- Children can successfully complete multi-turn conversations
- Requirements are accurately collected and confirmed
- Conversation flow feels natural and engaging
- System handles edge cases (vague responses, changes of mind)
- Performance remains acceptable with conversation state management

---

**Review this Spec and let me know if it captures your intent or if any changes are needed. Type 'GO!' when ready to proceed with implementation.** 