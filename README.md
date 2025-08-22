# Eva Coloring Sheet AI

An interactive AI coloring sheet creator for kids using agent-based architecture with voice interaction, AI image generation, and feedback loops.

## Features (Phase 1 - MVP)

✅ **Multi-Turn Conversations**: Natural back-and-forth dialogue to collect all requirements  
✅ **Voice Interaction**: Natural voice input using Whisper transcription  
✅ **AI Image Generation**: DALL-E 3 integration for creating coloring sheets  
✅ **Age-Appropriate Content**: Automatic filtering of inappropriate content  
✅ **Smart Conversation Processing**: Intelligent extraction of coloring requests  
✅ **Text-to-Speech**: Voice responses for engaging interaction  
✅ **Modern UI**: React frontend with conversation history and status tracking  
✅ **Session Management**: Maintains conversation state across multiple interactions  

## Quick Start

### Prerequisites

- Python 3.11.3 or higher
- OpenAI API key with access to DALL-E 3 and Whisper
- Node.js (version 14 or higher) - for React frontend

### Option 1: Gradio Interface (Simple)

1. Clone the repository:
```bash
git clone <repository-url>
cd eva-coloring-sheet-ai
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
# Create a .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

4. Run the application:
```bash
python main.py
```

5. Open your browser to the Gradio interface (usually http://localhost:7860)

### Option 2: React Frontend (Recommended for Kids)

1. Clone the repository:
```bash
git clone <repository-url>
cd eva-coloring-sheet-ai
```

2. Install Python dependencies:
```bash
pip install -e .
pip install flask flask-cors
```

3. Set up environment variables:
```bash
# Create a .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

4. Start the Python API server:
```bash
python api_server.py
```

5. Install and start the React frontend:
```bash
cd frontend
npm install
npm start
```

6. Open your browser to the React interface (http://localhost:3000)

**Note:** The React frontend provides a much better user experience with proper toggle recording functionality!

## How to Use

### Multi-Turn Conversation Flow

The system now supports natural multi-turn conversations! Here's how it works:

1. **Start a Conversation**: Click the microphone button and say what you want to color
   - Example: "I want a cat coloring sheet"

2. **Answer Questions**: The AI will ask clarifying questions to get all the details
   - "What kind of cat? A big cat like a lion or a small cat like a house cat?"
   - "What should the cat be doing? Sitting, sleeping, or playing?"
   - "What color should the cat be?"

3. **Confirm Your Choices**: When all details are collected, the AI will confirm with you
   - "Let me make sure I have everything right. You want an orange house cat playing with a ball. Is that correct?"

4. **Get Your Coloring Sheet**: After confirmation, the AI generates your personalized coloring sheet

### Example Conversation

```
👤 Child: "I want a cat coloring sheet"
🤖 AI: "Great! I'd love to help you create a cat coloring sheet. What kind of cat would you like? A big cat like a lion or a small cat like a house cat?"

👤 Child: "A house cat"
🤖 AI: "Perfect! A house cat it is. What should the cat be doing? Should it be sitting, sleeping, or playing?"

👤 Child: "Playing with a ball"
🤖 AI: "That sounds fun! A house cat playing with a ball. What color should the cat be?"

👤 Child: "Orange"
🤖 AI: "An orange house cat playing with a ball - that's going to be great! Is there anything else you'd like to add to your coloring sheet?"

👤 Child: "No, that's perfect"
🤖 AI: "Let me make sure I have everything right. You want a coloring sheet of an orange house cat playing with a ball. Is that correct?"

👤 Child: "Yes"
🤖 AI: "Perfect! I'll create your orange cat playing with a ball coloring sheet now. This might take a moment..."
```

### Conversation Controls

- **Reset Conversation**: Start over with a new coloring sheet request
- **New Conversation**: Begin a completely fresh session
- **Status Tracking**: See the current phase of your conversation (collecting, confirming, generating)

### Safety Features**: The system automatically:
   - Filters inappropriate content
   - Provides safe alternatives for blocked requests
   - Ensures all content is suitable for children aged 6-8

## Architecture

### Agent Structure

- **Voice Assistant Agent**: Handles voice interaction and coordinates other agents
- **Conversation Summarizer Agent**: Converts voice input to structured prompts
- **Coloring Sheet Designer Agent**: Generates images using DALL-E 3

### Data Flow

```
Voice Input → Transcription → Summarizer → Designer → Image Display
                                                      ↓
                                              Voice Response
```

### Key Components

- `src/agents/`: Specialized agents for different tasks
- `src/tools/`: DALL-E integration tool
- `src/utils/`: Audio processing utilities
- `src/ui/`: Gradio interface
- `src/crews/`: CrewAI orchestration

## Testing

### Run All Tests

```bash
uv run python -m pytest tests/ -v
```

### Test Multi-Turn Conversation

```bash
uv run python demo_multi_turn.py
```

### Test Coverage

- **Unit Tests**: Individual agent functionality
- **Integration Tests**: Complete workflow testing
- **Multi-Turn Tests**: Conversation state management and flow
- **Safety Tests**: Content filtering validation

## Development

### Project Structure

```
src/
├── agents/
│   ├── conversation_summarizer.py
│   └── coloring_sheet_designer.py
├── crews/
│   ├── coloring_sheet_crew.py
│   └── config/
├── tools/
│   └── dalle_tool.py
├── utils/
│   └── audio_utils.py
└── ui/
    └── interface.py
```

### Adding New Features

1. Create new agents in `src/agents/`
2. Add tools in `src/tools/`
3. Update the crew in `src/crews/coloring_sheet_crew.py`
4. Add tests in `tests/`

## Safety & Content Filtering

The system includes comprehensive safety measures:

- **Inappropriate Content Detection**: Filters out violence, weapons, adult content
- **Age-Appropriate Prompts**: Ensures all content is suitable for children
- **Fallback Mechanisms**: Provides safe alternatives when requests are blocked
- **Error Handling**: Graceful degradation when services fail

## Future Phases

### Phase 2: Feedback Loop System
- Allow children to provide feedback on generated images
- Implement image editing based on feedback
- Support multiple iterations

### Phase 3: Personalization & Smart Interaction
- User profile system
- Emotion detection from voice
- Smart prompting and suggestions

### Phase 4: Printing & Export Features
- One-click printing of coloring sheets
- Multiple export formats
- Print optimization

### Phase 5: Advanced Features & Polish
- Multi-language support
- Accessibility features
- Performance optimization

## Contributing

1. Follow the existing code structure and conventions
2. Add comprehensive tests for new features
3. Ensure all content filtering and safety measures are maintained
4. Update documentation for any new features

## License

[Add your license information here]

## Support

For issues and questions, please [create an issue](link-to-issues) in the repository.





