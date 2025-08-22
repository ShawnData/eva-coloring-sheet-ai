from crewai import Agent, Task, Crew, Process
from src.tools.dalle_tool import dalle_tool
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)

# --- Agent Definitions ---

voice_agent = Agent(
    role="Voice Assistant",
    goal="Facilitate natural, child-friendly voice-based interaction and collect coloring sheet requirements",
    backstory="""You are a friendly, patient voice assistant who helps children create coloring sheets. You greet, clarify, and guide the child through the process, making sure they feel heard and encouraged. You collect all the requirements from the child and create a clear prompt for the designer.""",
    verbose=True,
    allow_delegation=True
)

designer_agent = Agent(
    role="Coloring Sheet Designer",
    goal="Generate high-quality, age-appropriate coloring sheet images that children will enjoy coloring.",
    backstory="""You are a skilled digital artist specializing in creating coloring sheets for children. You understand what makes a good coloring sheet: clear lines, simple shapes, age-appropriate content, and engaging designs that encourage creativity. You work with DALL-E to bring children's imaginations to life.""",
    verbose=True,
    allow_delegation=False,
    tools=[dalle_tool]
)

# --- Task Definitions ---

voice_interaction_task = Task(
    description="""
    Interact with the child through voice input and collect all requirements for their coloring sheet.
    
    Input: {voice_input}
    
    Your responsibilities:
    1. Greet the child warmly
    2. Listen to their request for a coloring sheet
    3. Ask clarifying questions if needed (what kind of animal, object, or scene they want)
    4. Collect all the details they want in their coloring sheet
    5. Create a clear, structured prompt for the designer
    
    You must respond with a JSON object in this exact format:
    {
        "message": "friendly response to the child explaining what you're going to create",
        "prompt": "clear, detailed prompt for the designer to create the coloring sheet",
        "error": null
    }
    
    If the child doesn't want a coloring sheet or there's an error, set prompt to null and provide an appropriate message.
    """,
    agent=voice_agent,
    expected_output="JSON object with conversation results and prompt for designer"
)

generate_coloring_sheet_task = Task(
    description="""
    Generate a coloring sheet image based on the prompt from the voice agent.
    
    IMPORTANT: The previous task returns a JSON object. You must extract the "prompt" field from that JSON and pass ONLY the string value to the DALL-E tool.
    
    Example:
    - If previous task returns: {"message": "...", "prompt": "a happy cat", "error": null}
    - You should use: "a happy cat" as the prompt for the DALL-E tool
    
    The DALL-E tool will handle content safety and coloring sheet optimization.
    
    You must respond with a JSON object in this exact format:
    {
        "success": true/false,
        "image_url": "URL of generated image or null",
        "message": "friendly message to the child about their coloring sheet",
        "error": "error message if failed or null"
    }
    
    If successful, provide a cheerful message about the coloring sheet. If failed, provide a friendly explanation.
    """,
    agent=designer_agent,
    expected_output="JSON object with image generation results"
)

# --- Crew Definition ---

def create_coloring_sheet_crew():
    return Crew(
        agents=[voice_agent, designer_agent],
        tasks=[voice_interaction_task, generate_coloring_sheet_task],
        process=Process.sequential,
        verbose=True,
    )