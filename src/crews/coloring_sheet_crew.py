from crewai import Task, Agent, Crew, Process
from typing import List, Dict, Any
from src.agents.conversation_summarizer import ConversationSummarizerAgent
from src.agents.coloring_sheet_designer import ColoringSheetDesignerAgent
from src.agents.voice_assistant import VoiceAssistantAgent
from src.tools.dalle_tool import dalle_tool

class ColoringSheetCrew:
    """A crew that designs a coloring sheet prompt and generates a coloring sheet"""
    
    def __init__(self):
        # Initialize agent classes
        self.summarizer_agent = ConversationSummarizerAgent()
        self.designer_agent = ColoringSheetDesignerAgent()
        self.voice_assistant_agent = VoiceAssistantAgent()
        
        # Create agents with tools
        self.voice_assistant = self.voice_assistant_agent.create_agent()
        
        self.conversation_summarizer = Agent(
            role="Conversation Summarizer",
            goal="Convert child's voice input into structured, age-appropriate prompts for coloring sheet generation",
            backstory="""You are an expert at understanding children's requests and converting them into 
            clear, structured prompts for image generation. You excel at filtering inappropriate content 
            and ensuring all prompts are suitable for children aged 6-8. You understand child psychology 
            and can interpret vague requests into specific, actionable descriptions.""",
            verbose=True,
            allow_delegation=False
        )
        
        self.coloring_sheet_designer = Agent(
            role="Coloring Sheet Designer",
            goal="Generate high-quality, age-appropriate coloring sheet images that children will enjoy coloring",
            backstory="""You are a skilled digital artist specializing in creating coloring sheets for children. 
            You understand what makes a good coloring sheet: clear lines, simple shapes, age-appropriate content, 
            and engaging designs that encourage creativity. You work with DALL-E to bring children's imaginations to life.""",
            verbose=True,
            allow_delegation=False,
            tools=[dalle_tool]
        )
        
        # Create tasks
        self.summarize_conversation_task = Task(
            description="""
            Analyze the child's voice input and determine if they want a coloring sheet.
            If they do, extract the subject and create a structured prompt.
            If they don't, provide an appropriate response.
            
            Input: {transcription}
            
            You must respond with a JSON object in this exact format:
            {
                "is_coloring_request": true/false,
                "message": "response to child",
                "prompt": "structured prompt for image generation or null",
                "confidence": 0.0-1.0
            }
            
            Examples:
            - If child says "I want a cat coloring sheet" → {"is_coloring_request": true, "message": "Great! I'll create a cat coloring sheet for you!", "prompt": "friendly cartoon cat", "confidence": 0.9}
            - If child says "Hello" → {"is_coloring_request": false, "message": "Hello! I'm here to help you create coloring sheets!", "prompt": null, "confidence": 0.0}
            """,
            agent=self.conversation_summarizer,
            expected_output="JSON object with conversation analysis results"
        )

        self.generate_coloring_sheet_task = Task(
            description="""
            Generate a coloring sheet image based on the structured prompt from the previous task.
            Use the DALL-E tool to create the image.
            
            Input: {prompt}
            
            You must respond with a JSON object in this exact format:
            {
                "success": true/false,
                "image_url": "URL of generated image or null",
                "message": "response to child",
                "error": "error message if failed or null"
            }
            
            If successful, use the generate_coloring_sheet tool with the prompt to create the image.
            """,
            agent=self.coloring_sheet_designer,
            expected_output="JSON object with image generation results"
        )

    def crew(self) -> Crew:
        """Creates and returns a Crew instance with configured agents and tasks."""
        return Crew(
            agents=[self.voice_assistant, self.conversation_summarizer, self.coloring_sheet_designer],
            tasks=[self.summarize_conversation_task, self.generate_coloring_sheet_task],
            process=Process.sequential,
            memory=True,  
            verbose=True,
        )
    
    def process_voice_input(self, transcription: str) -> Dict[str, Any]:
        """
        Process voice input and generate coloring sheet if requested
        
        Args:
            transcription: Raw voice transcription from child
            
        Returns:
            Dict containing response message and image URL if applicable
        """
        try:
            # Use the voice assistant agent to process the input
            return self.voice_assistant_agent.process_voice_input(transcription)
                    
        except Exception as e:
            return {
                "message": "Oops! Something went wrong. Let's try again!",
                "image_url": None,
                "error": str(e)
            }