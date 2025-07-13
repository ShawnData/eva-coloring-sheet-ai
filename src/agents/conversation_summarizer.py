from crewai import Agent
from typing import Dict, Any
import re

class ConversationSummarizerAgent:
    """
    Agent that converts child's voice input to structured prompts for image generation.
    Filters inappropriate content and creates age-appropriate prompts.
    """
    
    def __init__(self):
        self.age_group = "6-8"  # Target age group
        self.inappropriate_content = [
            'violence', 'weapon', 'gun', 'knife', 'blood', 'death', 'scary',
            'monster', 'ghost', 'zombie', 'vampire', 'witch', 'evil', 'dark',
            'adult', 'sexy', 'nude', 'alcohol', 'drug', 'smoke', 'kill', 'fight'
        ]
        
    def create_agent(self) -> Agent:
        """Create the Conversation Summarizer Agent"""
        return Agent(
            role="Conversation Summarizer",
            goal="Convert child's voice input into structured, age-appropriate prompts for coloring sheet generation",
            backstory="""You are an expert at understanding children's requests and converting them into 
            clear, structured prompts for image generation. You excel at filtering inappropriate content 
            and ensuring all prompts are suitable for children aged 6-8. You understand child psychology 
            and can interpret vague requests into specific, actionable descriptions.""",
            verbose=True,
            allow_delegation=False,
            tools=[]  # No external tools needed for this agent
        )
    
    def summarize_conversation(self, transcription: str) -> Dict[str, Any]:
        """
        Convert voice transcription into structured prompt data
        
        Args:
            transcription: Raw voice transcription from child
            
        Returns:
            Dict containing structured prompt information
        """
        # Clean and normalize the transcription
        cleaned_text = self._clean_transcription(transcription)
        
        # Check for coloring sheet requests
        if not self._is_coloring_sheet_request(cleaned_text):
            return {
                "is_coloring_request": False,
                "message": "I understand you're talking to me! If you'd like a coloring sheet, just tell me what you'd like to see.",
                "prompt": None,
                "confidence": 0.0
            }
        
        # Extract the main subject/object
        subject = self._extract_subject(cleaned_text)
        
        # Filter for inappropriate content
        if self._contains_inappropriate_content(subject):
            return {
                "is_coloring_request": True,
                "message": "I'd love to make you a coloring sheet! How about a friendly animal or a fun character instead?",
                "prompt": "friendly cartoon animal",
                "confidence": 0.8
            }
        
        # Create structured prompt
        structured_prompt = self._create_structured_prompt(subject, cleaned_text)
        
        return {
            "is_coloring_request": True,
            "message": f"Great! I'll create a coloring sheet of {subject} for you!",
            "prompt": structured_prompt,
            "confidence": self._calculate_confidence(cleaned_text),
            "original_request": cleaned_text
        }
    
    def _clean_transcription(self, text: str) -> str:
        """Clean and normalize transcription text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove common filler words
        filler_words = ['um', 'uh', 'like', 'you know', 'i mean']
        for word in filler_words:
            text = text.replace(word, '')
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _is_coloring_sheet_request(self, text: str) -> bool:
        """Check if the text contains a coloring sheet request"""
        coloring_keywords = [
            'coloring', 'color', 'draw', 'picture', 'sheet', 'page',
            'make me', 'create', 'want', 'like to see', 'show me'
        ]
        
        return any(keyword in text for keyword in coloring_keywords)
    
    def _extract_subject(self, text: str) -> str:
        """Extract the main subject/object from the request"""
        # Common patterns for subject extraction
        patterns = [
            r'(?:i want|make me|create|draw|show me)\s+(?:a\s+)?(.+)',
            r'(?:coloring sheet|picture|drawing)\s+(?:of\s+)?(.+)',
            r'(.+?)\s+(?:coloring|picture|drawing)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                subject = match.group(1).strip()
                # Clean up common endings
                subject = re.sub(r'\s+(?:please|thanks|thank you|for me)$', '', subject)
                return subject
        
        # Fallback: take the last few words
        words = text.split()
        if len(words) <= 3:
            return text
        return ' '.join(words[-3:])
    
    def _contains_inappropriate_content(self, text: str) -> bool:
        """Check if text contains inappropriate content"""
        text_lower = text.lower()
        return any(word in text_lower for word in self.inappropriate_content)
    
    def _create_structured_prompt(self, subject: str, original_text: str) -> str:
        """Create a structured prompt for image generation"""
        # Add age-appropriate modifiers
        modifiers = []
        
        # Add style modifiers based on context
        if any(word in original_text for word in ['cute', 'adorable', 'sweet']):
            modifiers.append('cute')
        if any(word in original_text for word in ['big', 'large', 'huge']):
            modifiers.append('large')
        if any(word in original_text for word in ['small', 'tiny', 'little']):
            modifiers.append('small')
        if any(word in original_text for word in ['happy', 'smiling', 'joyful']):
            modifiers.append('happy')
        
        # Build the prompt
        if modifiers:
            prompt = f"{' '.join(modifiers)} {subject}"
        else:
            prompt = f"friendly {subject}"
        
        return prompt
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate confidence score for the interpretation"""
        # Simple confidence scoring based on clarity
        clarity_indicators = [
            len(text.split()) >= 3,  # Has enough words
            any(word in text for word in ['want', 'make', 'create', 'draw']),  # Clear intent
            not any(word in text for word in ['maybe', 'perhaps', 'i think', 'not sure'])  # Not uncertain
        ]
        
        confidence = sum(clarity_indicators) / len(clarity_indicators)
        return min(confidence, 0.95)  # Cap at 95% 