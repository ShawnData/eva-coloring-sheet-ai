# Spec: Conversation Requirements Collection Enhancement

## Purpose & User Problem
The voice agent currently collects requirements in a structured format but doesn't effectively extract and organize keywords from conversations. When the child wants to generate an image, the system should have a clear list of keywords (e.g., ["cute cat", "rainbow", "playing"]) that can be passed to the designer agent for better prompt generation.

## Success Criteria
- Voice agent extracts keywords from all conversation turns
- Keywords are collected as a list (e.g., ["cute", "cat", "rainbow", "playing", "orange"])
- Keywords are maintained throughout the conversation session
- When image generation is requested, the complete keyword list is passed to the designer agent
- Designer agent uses the keyword list to create better DALL-E prompts
- Keywords are deduplicated and organized logically
- System maintains both structured requirements and keyword list for flexibility

## Scope & Constraints

### In Scope
- Enhance `ConversationState` to include a `keywords` list
- Improve `extract_requirements_from_text()` to also extract keywords
- Add keyword extraction from conversation history
- Update voice agent task to maintain keyword list
- Modify designer agent to receive and use keyword list
- Update conversation utilities to handle keyword management
- Add keyword deduplication and organization logic

### Out of Scope
- Advanced NLP keyword extraction (basic pattern matching is sufficient)
- Keyword weighting or scoring
- Persistent keyword storage across sessions
- Keyword-based image search or retrieval

## Technical Considerations

### Keyword Extraction Strategy
- Extract nouns, adjectives, and action words from voice input
- Maintain a comprehensive list of relevant keywords
- Deduplicate keywords while preserving context
- Organize keywords by category (subject, description, action, objects, colors)

### Conversation State Enhancement
```python
@dataclass
class ConversationState:
    requirements: Dict[str, Any] = field(default_factory=dict)
    keywords: List[str] = field(default_factory=list)  # NEW
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    # ... existing fields
```

### Keyword Categories
- **Subjects**: cat, dog, bird, etc.
- **Descriptions**: cute, big, small, friendly, etc.
- **Actions**: playing, sleeping, running, etc.
- **Objects**: ball, toy, flower, etc.
- **Colors**: red, blue, green, etc.

### Designer Agent Integration
- Receive keyword list as input
- Use keywords to enhance DALL-E prompt generation
- Maintain backward compatibility with existing requirements structure

## Implementation Plan

### Phase 1: Core Keyword Extraction
1. Enhance `ConversationState` with keywords list
2. Improve `extract_requirements_from_text()` to return keywords
3. Add keyword deduplication logic
4. Update conversation state management

### Phase 2: Voice Agent Integration
1. Modify voice agent task to maintain keyword list
2. Update conversation processing to extract keywords from each turn
3. Ensure keywords are preserved across conversation turns

### Phase 3: Designer Agent Enhancement
1. Update designer agent task to receive keyword list
2. Enhance prompt generation to use keywords effectively
3. Test keyword-based prompt generation

### Phase 4: Testing & Validation
1. Test keyword extraction from various conversation scenarios
2. Validate keyword list is passed correctly to designer agent
3. Ensure backward compatibility with existing functionality

## Example Conversation Flow

```
Child: "I want a cat coloring sheet"
Keywords: ["cat"]

Child: "A cute cat"
Keywords: ["cat", "cute"]

Child: "Playing with a rainbow"
Keywords: ["cat", "cute", "playing", "rainbow"]

Child: "That's all"
Keywords: ["cat", "cute", "playing", "rainbow"]
→ Pass to designer agent for image generation
```

## Success Metrics
- Keywords are correctly extracted from 90%+ of conversation inputs
- Keyword list is maintained accurately throughout conversation
- Designer agent receives complete keyword list when generating images
- Generated prompts are more detailed and accurate with keyword input
- System maintains backward compatibility with existing functionality

---

**Review this Spec and let me know if it captures your intent or if any changes are needed. Type 'GO!' when ready to proceed with implementation.** 