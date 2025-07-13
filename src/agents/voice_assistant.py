from crewai import Agent
from typing import Dict, Any, Optional
import logging
import os
import openai
from src.agents.conversation_summarizer import ConversationSummarizerAgent
from src.agents.coloring_sheet_designer import ColoringSheetDesignerAgent

class VoiceAssistantAgent:
    """
    Voice Assistant Agent that coordinates with other agents to handle voice interactions
    and coloring sheet generation requests using LLM for intelligent conversation.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.summarizer_agent = ConversationSummarizerAgent()
        self.designer_agent = ColoringSheetDesignerAgent()
        
        # Initialize OpenAI client for LLM conversation
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.openai_client = openai.OpenAI(api_key=api_key)
        
        # Conversation context for maintaining context
        self.conversation_history = []
        
    def create_agent(self) -> Agent:
        """Create the Voice Assistant Agent"""
        return Agent(
            role="Voice Interaction Specialist",
            goal="Facilitate natural voice-based interaction with children, understand their requests, and coordinate with other agents to fulfill coloring sheet requests",
            backstory="""You are a friendly, patient voice interaction specialist who excels at communicating with children. 
            You have a natural ability to understand and adapt to different age groups, making complex concepts simple and engaging. 
            You can analyze voice input, determine if children want coloring sheets, and coordinate with other agents to fulfill their requests.
            You always respond in a child-friendly, encouraging manner.""",
            verbose=True,
            allow_delegation=True
        )
    
    def process_voice_input(self, transcription: str) -> Dict[str, Any]:
        """
        Process voice input and coordinate with other agents to fulfill requests
        
        Args:
            transcription: Raw voice transcription from child
            
        Returns:
            Dict containing response message and image URL if applicable
        """
        try:
            self.logger.info(f"Processing voice input: {transcription}")
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": transcription})
            
            # Step 1: Use conversation summarizer to analyze the input
            summarizer_result = self.summarizer_agent.summarize_conversation(transcription)
            
            # Step 2: Check if this is a coloring sheet request
            if not summarizer_result.get("is_coloring_request", False):
                # Handle general conversation with LLM
                return self._handle_general_conversation_with_llm(transcription, summarizer_result)
            
            # Step 3: Handle coloring sheet request
            return self._handle_coloring_sheet_request(transcription, summarizer_result)
            
        except Exception as e:
            self.logger.error(f"Error processing voice input: {str(e)}")
            return {
                "message": "Oops! Something went wrong. Let's try again!",
                "image_url": None,
                "error": str(e)
            }
    
    def _handle_general_conversation_with_llm(self, transcription: str, summarizer_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle general conversation using LLM for intelligent responses
        
        Args:
            transcription: Original voice input
            summarizer_result: Results from conversation summarizer
            
        Returns:
            Dict containing response message
        """
        try:
            # Prepare conversation context
            system_prompt = """You are Eva, a friendly AI assistant who helps children create coloring sheets. You are:

1. **Child-friendly**: Always speak in a warm, encouraging tone appropriate for children aged 6-8
2. **Conversational**: Engage in natural conversation, ask follow-up questions, show interest
3. **Helpful**: Guide children toward coloring sheet creation when appropriate
4. **Educational**: Make learning fun and interactive
5. **Safe**: Always provide age-appropriate responses

Your responses should be:
- 1-2 sentences long (appropriate for voice interaction)
- Conversational and engaging
- Encouraging of creativity
- Sometimes include gentle suggestions for coloring sheets

Examples of good responses:
- "Hello! I'm so happy to talk with you! What's your favorite animal?"
- "That sounds really fun! Would you like me to create a coloring sheet of that?"
- "I love that idea! Tell me more about what you're thinking."
- "You're so creative! What else would you like to talk about or create?"

Remember: You're talking to a child, so be patient, encouraging, and make them feel heard and valued."""

            # Build conversation messages with proper typing
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history (last 4 exchanges to maintain context)
            recent_history = self.conversation_history[-8:] if len(self.conversation_history) > 8 else self.conversation_history
            for msg in recent_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Get LLM response
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=100,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            message_content = response.choices[0].message.content
            message = message_content.strip() if message_content else "That's interesting! I'd love to help you create a coloring sheet. What would you like to see?"
            
            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": message})
            
            # Keep conversation history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return {
                "message": message,
                "image_url": None
            }
            
        except Exception as e:
            self.logger.error(f"Error in LLM conversation: {str(e)}")
            # Fallback to simple response
            return {
                "message": "That's interesting! I'd love to help you create a coloring sheet. What would you like to see?",
                "image_url": None
            }
    
    def _handle_coloring_sheet_request(self, transcription: str, summarizer_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle coloring sheet generation requests
        
        Args:
            transcription: Original voice input
            summarizer_result: Results from conversation summarizer
            
        Returns:
            Dict containing response message and image URL
        """
        prompt = summarizer_result.get("prompt")
        confidence = summarizer_result.get("confidence", 0.8)
        
        if not prompt:
            # Use LLM to ask for clarification
            clarification_message = self._get_clarification_with_llm(transcription)
            return {
                "message": clarification_message,
                "image_url": None
            }
        
        # Step 4: Use coloring sheet designer to generate the image
        self.logger.info(f"Generating coloring sheet with prompt: {prompt}")
        designer_result = self.designer_agent.generate_coloring_sheet(prompt, confidence)
        
        # Step 5: Create engaging response with LLM
        if designer_result.get("success", False):
            success_message = self._get_success_message_with_llm(transcription, prompt, designer_result)
            return {
                "message": success_message,
                "image_url": designer_result.get("image_url")
            }
        else:
            # Try fallback if original failed
            self.logger.info("Original generation failed, trying fallback")
            fallback_result = self.designer_agent.retry_with_fallback(prompt)
            if fallback_result.get("success", False):
                fallback_message = self._get_fallback_message_with_llm(transcription, fallback_result)
                return {
                    "message": fallback_message,
                    "image_url": fallback_result.get("image_url")
                }
            else:
                error_message = self._get_error_message_with_llm(transcription)
                return {
                    "message": error_message,
                    "image_url": None
                }
    
    def _get_clarification_with_llm(self, transcription: str) -> str:
        """Get clarification using LLM when prompt is unclear"""
        try:
            system_prompt = """You are Eva, a friendly AI assistant. The child's request for a coloring sheet wasn't clear enough. 
            Ask a friendly, specific question to help them clarify what they want. Be encouraging and give examples."""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Child said: '{transcription}' but I need more details to create a coloring sheet. Ask a friendly question to help them clarify."}
                ],
                max_tokens=80,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else "I'd love to make you a coloring sheet! What would you like to see?"
        except Exception as e:
            return "I'd love to make you a coloring sheet! What would you like to see?"
    
    def _get_success_message_with_llm(self, transcription: str, prompt: str, designer_result: Dict[str, Any]) -> str:
        """Get engaging success message using LLM"""
        try:
            system_prompt = """You are Eva, a friendly AI assistant. The child just got a coloring sheet they requested. 
            Give them an enthusiastic, encouraging response about their new coloring sheet. Be specific about what they got."""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Child requested: '{transcription}' and got a coloring sheet of '{prompt}'. Give them an enthusiastic response."}
                ],
                max_tokens=80,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else f"Here's your {prompt} coloring sheet! I hope you love it!"
        except Exception as e:
            return f"Here's your {prompt} coloring sheet! I hope you love it!"
    
    def _get_fallback_message_with_llm(self, transcription: str, fallback_result: Dict[str, Any]) -> str:
        """Get message for fallback coloring sheet"""
        try:
            system_prompt = """You are Eva, a friendly AI assistant. The child's original request couldn't be fulfilled, 
            but you created a special alternative coloring sheet for them. Be encouraging and make them feel special."""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Child requested: '{transcription}' but I made them a special alternative coloring sheet instead. Give them an encouraging response."}
                ],
                max_tokens=80,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else "I made you a special coloring sheet instead! I hope you like it!"
        except Exception as e:
            return "I made you a special coloring sheet instead! I hope you like it!"
    
    def _get_error_message_with_llm(self, transcription: str) -> str:
        """Get encouraging error message using LLM"""
        try:
            system_prompt = """You are Eva, a friendly AI assistant. Something went wrong creating the coloring sheet. 
            Be encouraging and suggest trying something else. Don't make the child feel bad about the error."""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Child requested: '{transcription}' but I couldn't create the coloring sheet. Give them an encouraging response and suggest trying something else."}
                ],
                max_tokens=80,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else "I'm sorry, I couldn't create that coloring sheet right now. Let's try something else!"
        except Exception as e:
            return "I'm sorry, I couldn't create that coloring sheet right now. Let's try something else!"
    
    def get_agent_tools(self) -> list:
        """
        Get tools that this agent can use
        
        Returns:
            List of tools available to this agent
        """
        # This agent doesn't need direct tools as it coordinates with other agents
        return []
    
    def get_agent_dependencies(self) -> list:
        """
        Get other agents this agent depends on
        
        Returns:
            List of agent dependencies
        """
        return [self.summarizer_agent, self.designer_agent] 