from crewai import Agent, Task, Crew, Process
from src.tools.dalle_tool import dalle_tool
from src.utils.conversation_utils import ConversationState 
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)

# --- Agent Definitions ---

voice_agent = Agent(
    role="Voice Assistant",
    goal="Facilitate natural, child-friendly multi-turn conversations to collect all coloring sheet requirements and summarize them as a single prompt.",
    backstory="""You are a friendly, patient voice assistant who helps children create coloring sheets through natural conversation. You engage in multiple back-and-forth interactions to collect all the details the child wants, extract keywords from their speech, ask clarifying questions when needed, and confirm the final requirements before proceeding to image generation. You make sure children feel heard and encouraged throughout the process.""",
    verbose=False,
    allow_delegation=True
)

designer_agent = Agent(
    role="Coloring Sheet Designer",
    goal="Generate high-quality, age-appropriate coloring sheet images based on the prompt from the voice agent.",
    backstory="""You are a skilled digital artist specializing in designing coloring sheets for children. You only generate images when you receive complete, confirmed summary from the voice agent. You understand what makes a good coloring sheet: clear lines, simple shapes, age-appropriate content, and engaging designs that encourage creativity. You work with DALL-E to bring children's imaginations to life.""",
    verbose=False,
    allow_delegation=False,
    tools=[dalle_tool]
)

# --- Task Definitions ---

voice_interaction_task = Task(
    description="""
    Engage in multi-turn conversation with the child to collect all requirements and keywords for their coloring sheet.
    
    The child just said: {voice_input}
    
    Current conversation state: {conversation_state}
    
    CRITICAL: You MUST respond to the child's voice_input. Do NOT give generic responses!
    
    Your responsibilities:
    0. Read the current conversation state
    1. FIRST: Read and understand the child's voice_input - this is what they just said to you
    2. Identify requirements from their voice_input 
    3. Update the conversation state with any new requirements found into the summary field
    4. Determine if they want to generate the image or need more questions
    5. Provide a brief, friendly response that directly addresses their input
    
    IMPORTANT RULES:
    - Keep responses SHORT and friendly (1-2 sentences max)
    - NEVER give generic responses like "What would you like on your coloring sheet?"
    - ALWAYS acknowledge what the child just said
    - If they say "that's all", "generate", "create", "make it", or similar - they want the image generated!
    - Only ask 1 question at a time, not multiple questions
    - If they mention an animal/object, ask for ONE detail only
    - ALWAYS extract keywords from their input and add them to the conversation state
    
    Conversation Flow:
    - FIRST TURN: If this is the first time (empty conversation_state), acknowledge their request and ask for details
    - NOT FIRST TURN: Read the summary field in the current conversation state and use it to continue collecting requirements from the child
    - If requirements are incomplete: Ask clarifying questions and continue collecting
    - If requirements seem complete: Confirm with the child before proceeding
    - If child confirms: Mark conversation as ready for image generation, and 
    - If child wants changes: Update summary and continue conversation
    
    NOTE: Do not ask what color, they will all be black or white since this is a coloring sheet. 
    
    You must respond with a JSON object in this exact format:
    {
        "message": "friendly response to the child",
        "conversation_state": {
            "summary": "...",
            "conversation_history": [...],
            "is_complete": true/false,
            "is_confirmed": true/false,
            "current_phase": "collecting/confirming/generating",
            "session_id": "..."
        },
        "should_generate_image": true/false,
        "error": null
    }
    
    EXAMPLES - COPY THESE EXACT PATTERNS:
    
    If child says "I want a cat coloring sheet":
    {
        "message": "Great! Anything else you want to add?",
        "conversation_state": {
            "summary": "a cat",
            "conversation_history": [],
            "is_complete": false,
            "is_confirmed": false,
            "current_phase": "collecting",
            "session_id": "1"
        },
        "should_generate_image": false,
        "error": null
    }
    
    If child says "That's all I need" or "Generate the image" or "Create it":
    {
        "message": "Perfect! Creating your coloring sheet now!",
        "conversation_state": {
            "summary": "a cute cat with rainbow in the background",
            "conversation_history": [],
            "is_complete": true,
            "is_confirmed": true,
            "current_phase": "generating",
            "session_id": "1"
        },
        "should_generate_image": true,
        "error": null
    }
    
    CRITICAL: If they say words like "that's all", "generate", "create", "make it", "done", "ready" - SET should_generate_image to TRUE!
    CRITICAL: ALWAYS include the keywords list in the conversation_state!
    """,
    agent=voice_agent,
    expected_output="JSON object with updated conversation state and response message"
)

generate_coloring_sheet_task = Task(
    description="""
    Design and Generate a coloring sheet image based on the summary field in the conversation state.
    IMPORTANT: The previous task returns a JSON object. You must extract the "summary" field from that JSON and pass ONLY the string value to the DALL-E tool.
    
    Current conversation state: {conversation_state}
    
    Process:
    1. Extract the summary prompt from the conversation state JSON
    2. Design a better prompt based on the summary prompt using your expertise
    3. Use the DALL-E tool to generate the coloring sheet based on the new prompt
    4. Return success result with the image URL
    
    Example:
    - If previous task returns: {"summary": "a fat white cat with a snowball"}
    - You should use: "{\"prompt\": \"a fat white cat with a snowball coloring sheet\"}" as the Tool Input for the DALL-E tool
    
    The DALL-E tool will handle content safety and coloring sheet optimization.
   
    Always create the DALL-E prompt using the summary prompt, then use the dalle_tool to generate the image suitable for use as a coloring page.
    
    You must respond with a JSON object in this exact format:
    {
        "success": true/false,
        "image_url": "URL of generated image or null",
        "message": "Here's your coloring sheet! Have fun coloring!",
        "error": "error message if failed or null"
    }
    
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
        verbose=False,
    )

def process_conversation_turn(crew, voice_input: str, conversation_state: ConversationState = None) -> dict:
    """
    Process a single turn in the conversation.
    
    Args:
        crew: The CrewAI crew instance
        voice_input: The child's voice input
        conversation_state: Current conversation state (None for new conversation)
    
    Returns:
        Dictionary with response message, updated conversation state, and image URL if generated
    """
    
    # Initialize conversation state if this is the first turn
    if conversation_state is None:
        conversation_state = ConversationState()
    
    # Prepare inputs for the crew
    inputs = {
        "voice_input": voice_input,
        "conversation_state": json.dumps(conversation_state.to_dict())
    }
    
    # Debug: Print what we're sending to the agent
    logger.info(f"DEBUG: Sending to agent - voice_input: '{voice_input}'")
    logger.info(f"DEBUG: Sending to agent - conversation_state: {inputs['conversation_state']}")
    
    try:
        # Run only the voice interaction task first
        voice_crew = Crew(
            agents=[voice_agent],
            tasks=[voice_interaction_task],
            process=Process.sequential,
            verbose=True,
        )
        
        voice_output = voice_crew.kickoff(inputs=inputs)
        
        # Parse the voice agent output
        if hasattr(voice_output, 'raw') and voice_output.raw:
            # Try to parse the raw output as JSON
            try:
                raw_str = voice_output.raw.strip()
                if raw_str.startswith('```json'):
                    raw_str = raw_str[7:]
                if raw_str.endswith('```'):
                    raw_str = raw_str[:-3]
                
                result = json.loads(raw_str.strip())
            except json.JSONDecodeError:
                # If not valid JSON, create a basic response
                result = {
                    "message": voice_output.raw,
                    "conversation_state": conversation_state.to_dict(),
                    "should_generate_image": False,
                    "error": "Failed to parse output"
                }
        else:
            # Fallback to to_dict() method
            result = voice_output.to_dict()
            if isinstance(result, dict) and 'tasks_outputs' in result:
                # Extract from task outputs
                task_outputs = result['tasks_outputs']
                if task_outputs and len(task_outputs) > 0:
                    last_output = task_outputs[-1]
                    if isinstance(last_output, str):
                        try:
                            result = json.loads(last_output)
                        except json.JSONDecodeError:
                            result = {
                                "message": last_output,
                                "conversation_state": conversation_state.to_dict(),
                                "should_generate_image": False,
                                "error": None
                            }
        
        # Extract the response components
        message = result.get("message", "I'm sorry, I couldn't process your request.")
        should_generate_image = result.get("should_generate_image", False)
        error = result.get("error")
        
        # Update conversation state if provided
        if "conversation_state" in result:
            updated_state = ConversationState.from_dict(result["conversation_state"])
            conversation_state = updated_state
        
        # Add both the user's input and the assistant's response to conversation history
        conversation_state.add_message("user", voice_input)
        conversation_state.add_message("assistant", message)
        
        # Generate image if requested
        image_url = None
        if should_generate_image and not error:
            try:
                # Create image generation crew
                image_crew = Crew(
                    agents=[designer_agent],
                    tasks=[generate_coloring_sheet_task],
                    process=Process.sequential,
                    verbose=True,
                )
                
                image_inputs = {
                    "conversation_state": json.dumps(conversation_state.to_dict())
                }
                
                image_output = image_crew.kickoff(inputs=image_inputs)
                
                # Parse image generation result
                if hasattr(image_output, 'raw') and image_output.raw:
                    try:
                        raw_str = image_output.raw.strip()
                        if raw_str.startswith('```json'):
                            raw_str = raw_str[7:]
                        if raw_str.endswith('```'):
                            raw_str = raw_str[:-3]
                        
                        image_result = json.loads(raw_str.strip())
                        image_url = image_result.get("image_url")
                        if image_result.get("success") and image_url:
                            message = image_result.get("message", message)
                        elif image_result.get("error"):
                            error = image_result.get("error")
                    except json.JSONDecodeError:
                        error = "Failed to parse image generation result"
            except Exception as e:
                logger.error(f"Error generating image: {str(e)}")
                error = f"Failed to generate image: {str(e)}"
        
        # Return the result
        return {
            "message": message,
            "conversation_state": conversation_state,
            "should_generate_image": should_generate_image,
            "error": error,
            "image_url": image_url
        }
        
    except Exception as e:
        logger.error(f"Error processing conversation turn: {str(e)}")
        return {
            "message": "I'm sorry, I had trouble understanding that. Please try again!",
            "conversation_state": conversation_state,
            "should_generate_image": False,
            "error": str(e),
            "image_url": None
        }