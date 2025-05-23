# Eva's Coloring Sheet AI

An Interactive AI Coloring Sheet Creator for Kids

## Project Goals
- Create an interactive AI to generate coloring sheets for my daugther, Eva.
- Learn more about agentic frameworks
- Learn effective use of Cursor IDE

## Overview

This project is an agent-based, voice-interactive system that allows children to create personalized coloring sheets through natural conversation. The system consists of multiple specialized agents collaborating in a modular workflow. It leverages speech recognition, natural language understanding, image generation, and user feedback loops to create and refine coloring sheets in an engaging and child-friendly manner.

## 📐 Architecture Overview:

```
graph TD
    A[Kid speaks to Voice Agent (Gradio Audio Input)]
    B[Voice Agent: Speech-to-Text (Whisper)]
    C[Summarizer Agent: Extract Requirements]
    D[Coloring Sheet Designer: Generate Image (DALL·E)]
    E[Gradio UI: Show Image Output]
    F[Kid speaks Feedback (Gradio Audio Input)]
    G[Feedback Interpreter Agent: Parse Feedback]
    H[Editor Agent: Edit Image (InstructPix2Pix)]
    I[Gradio UI: Show Edited Image]
    J[Print Agent: Send Image to Printer]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> B2[Speech-to-Text (Whisper) for Feedback]
    B2 --> G
    G --> H
    H --> I
    I --> F
    I --> J
```

**1. Voice Interaction Agent**
* Greets the child and initiates a creative prompt.

* Uses speech-to-text (STT) to transcribe the child’s voice input.

* Adapts language complexity and tone based on age.

* Offers choices and guides the conversation if needed (e.g., “Would you like animals, superheroes, or something else?”).

* Detects unclear or imaginative inputs and handles re-prompts gracefully.

* Sends conversation transcript to the Summarizer Agent.

**2. Conversation Summarizer Agent**
* Summarizes the voice interaction into a structured prompt/requirement (e.g., “a happy cat flying a spaceship over a rainbow”).

* Applies filters for age-appropriate and safe content.

* Corrects malformed or nonsensical prompts, adding contextual clarification if needed.

* Sends the sanitized, structured prompt to the Designer Agent.

**3. Coloring Sheet Designer Agent**
* Uses an image generation model (e.g., DALL·E, Stable Diffusion) to generate a black-and-white line-art image based on the structured prompt.

* Returns the image to the Voice Agent for review.

**4. Voice Interaction Agent (Feedback Loop)**
* Asks the child for feedback on the generated image.

* Uses STT again to capture response.

* Sends response to the Feedback Interpreter Agent.

**5. Feedback Interpreter Agent**
* Analyzes natural language feedback (e.g., “I want more stars” or “make it look happier”) and translates it into structured edit commands.

* Detects vague responses and triggers clarifying questions if needed.

* Sends edit instructions to the Editor Agent.

**6. Editor Agent**
* Applies edits to the original image using an image editing model or system.

* Returns the revised image for final review.

**7. Optional: Emotion Detection Module**
* (Bonus) Uses voice tone to detect frustration, joy, or confusion and adjusts the interaction accordingly.

**8. Optional: Personalization Module**
* Stores preferences (e.g., favorite themes or colors) for future interactions.

* Supports profile creation for recurring users.


## Key Features Summary
**🔊 1. Voice-Based Interaction**
* Kids interact with the system using natural voice input.

* Speech-to-text (STT) converts their ideas into text.

* Age-adaptive prompting and guidance ensure the experience is appropriate and engaging.

**📝 2. Conversation Summarization**
* Transcribes and summarizes the child’s creative intent into a clear, structured prompt.

* Automatically filters and adjusts content to keep it safe and appropriate for children.

**🎨 3. Coloring Sheet Generation**
* Uses AI image generation models to create black-and-white line art illustrations based on the summarized prompt.

* Supports whimsical and imaginative requests from kids.

**🔁 4. Feedback Collection and Iteration**
* After the initial image is shown, the child gives voice feedback (e.g., “I want a bigger sun”).

* System interprets vague or unclear feedback and may follow up for clarification.

**🖌️ 5. Image Editing**
* Applies feedback-driven edits using an image editing model (e.g., ControlNet, InstructPix2Pix).

* Maintains the coloring style (line art) after editing.

**😊 6. Personalization & Emotion Handling**
* Tracks preferences (e.g., favorite themes, colors) across sessions.

* Optional module detects emotions in voice to adapt the interaction dynamically (e.g., respond empathetically to frustration).

**🖨️ 7. Printing Integration**
* Provides a “Print My Coloring Sheet” feature after final approval.

* Connects to local or wireless printers (e.g., via WebUSB, IPP, or system print dialog).

* Ensures print-friendly layout with proper margins and orientation.

**🔧 8. Modular Agentic Architecture**
Each step is handled by a dedicated specialist agent:

 - Voice Agent

 - Summarizer Agent

 - Designer Agent

 - Feedback Interpreter

 - Editor Agent

 - Printer Agent (optional)


## Tech Stack
| Category                  | Tool/Library                 | Purpose/Notes                                 |
|---------------------------|-----------------------------|-----------------------------------------------|
| **Agent Orchestration**   | CrewAI                      | Modular agent orchestration, Python-native    |
| **LLM API**               | OpenAI GPT-4                | Powerful, easy-to-use language model API      |
| **Voice Input (STT)**     | OpenAI Whisper              | Accurate speech-to-text, straightforward setup|
| **Voice Output (TTS)**    | pyttsx3                    | Simple offline TTS, easy to install & run     |
| **Frontend UI**           | Gradio                      | Fast, minimal code to build voice/image UI    |
| **Image Generation**      | DALL·E (OpenAI API)         | Easy API for generating images from text      |
| **Image Editing**         | InstructPix2Pix             | Instruction-driven image editing via API      |
| **Printing**              | Browser's `window.print()`  | Simplest printing solution from web frontend  |
| **Data Storage**          | SQLite                      | Lightweight, file-based DB included in Python |
| **Image Utilities**       | Pillow                      | Popular Python imaging library, easy to use   |





