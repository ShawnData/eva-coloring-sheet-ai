from crewai import Agent
from typing import Dict, Any, Optional
import logging
from src.tools.dalle_tool import dalle_tool

class ColoringSheetDesignerAgent:
    """
    Agent that generates coloring sheet images using DALL-E.
    Ensures images are age-appropriate and suitable for coloring.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dalle_tool = dalle_tool
        
    def create_agent(self) -> Agent:
        """Create the Coloring Sheet Designer Agent"""
        return Agent(
            role="Coloring Sheet Designer",
            goal="Generate high-quality, age-appropriate coloring sheet images that children will enjoy coloring",
            backstory="""You are a skilled digital artist specializing in creating coloring sheets for children. 
            You understand what makes a good coloring sheet: clear lines, simple shapes, age-appropriate content, 
            and engaging designs that encourage creativity. You work with DALL-E to bring children's imaginations to life.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.dalle_tool]
        )
    
    def generate_coloring_sheet(self, prompt: str, confidence: float = 0.8) -> Dict[str, Any]:
        """
        Generate a coloring sheet image based on the provided prompt
        
        Args:
            prompt: Structured prompt for image generation
            confidence: Confidence score from conversation summarizer
            
        Returns:
            Dict containing image URL and metadata
        """
        try:
            # Validate prompt
            if not prompt or len(prompt.strip()) == 0:
                raise ValueError("Empty or invalid prompt provided")
            
            # Enhance prompt for better results
            enhanced_prompt = self._enhance_prompt(prompt)
            
            # Generate image using DALL-E tool
            self.logger.info(f"Generating coloring sheet with prompt: {enhanced_prompt}")
            
            # Use the DALL-E tool to generate the image
            image_url = self.dalle_tool._run(enhanced_prompt)
            
            if not image_url:
                raise Exception("No image URL returned from DALL-E")
            
            # Validate the generated image
            validation_result = self._validate_generated_image(image_url, prompt)
            
            return {
                "success": True,
                "image_url": image_url,
                "prompt_used": enhanced_prompt,
                "original_prompt": prompt,
                "confidence": confidence,
                "validation": validation_result,
                "message": f"Here's your coloring sheet! I created a {prompt} for you to color."
            }
            
        except Exception as e:
            self.logger.error(f"Error generating coloring sheet: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "I'm sorry, I couldn't create that coloring sheet right now. Let's try something else!",
                "fallback_prompt": self._get_fallback_prompt(prompt)
            }
    
    def _enhance_prompt(self, base_prompt: str) -> str:
        """
        Enhance the base prompt for better DALL-E results
        
        Args:
            base_prompt: Original prompt from conversation summarizer
            
        Returns:
            str: Enhanced prompt for DALL-E
        """
        # Add coloring sheet specific enhancements
        enhancements = [
            "black and white line art",
            "simple cartoon style",
            "large coloring areas",
            "clear bold outlines",
            "no shading or complex details",
            "child-friendly design"
        ]
        
        # Combine base prompt with enhancements
        enhanced = f"{base_prompt}, {' '.join(enhancements)}"
        
        # Ensure it's not too long (DALL-E has prompt length limits)
        if len(enhanced) > 1000:
            # Truncate while keeping the most important parts
            words = enhanced.split()
            if len(words) > 50:
                enhanced = ' '.join(words[:50]) + ', black and white line art, simple cartoon style'
        
        return enhanced
    
    def _validate_generated_image(self, image_url: str, original_prompt: str) -> Dict[str, Any]:
        """
        Validate that the generated image meets our requirements
        
        Args:
            image_url: URL of the generated image
            original_prompt: Original prompt used for generation
            
        Returns:
            Dict containing validation results
        """
        # For now, we'll do basic validation
        # In a production system, you might want to use image analysis APIs
        validation = {
            "url_valid": bool(image_url and image_url.startswith('http')),
            "prompt_alignment": self._check_prompt_alignment(original_prompt, image_url),
            "age_appropriate": True,  # DALL-E tool already filters for this
            "coloring_suitable": True  # DALL-E tool already optimizes for this
        }
        
        return validation
    
    def _check_prompt_alignment(self, prompt: str, image_url: str) -> bool:
        """
        Basic check if the generated image aligns with the prompt
        This is a simplified check - in production you might use image analysis
        """
        # For now, we'll assume alignment if we got a valid URL
        # In a real implementation, you might use image analysis APIs
        return bool(image_url and image_url.startswith('http'))
    
    def _get_fallback_prompt(self, original_prompt: str) -> str:
        """
        Generate a fallback prompt if the original fails
        
        Args:
            original_prompt: Original prompt that failed
            
        Returns:
            str: Safe fallback prompt
        """
        # Simple fallback prompts for common categories
        fallbacks = {
            'animal': 'friendly cartoon cat',
            'character': 'happy cartoon character',
            'vehicle': 'simple cartoon car',
            'nature': 'simple flower',
            'food': 'simple apple',
            'object': 'simple star'
        }
        
        # Try to match the original prompt to a category
        original_lower = original_prompt.lower()
        for category, fallback in fallbacks.items():
            if category in original_lower:
                return fallback
        
        # Default fallback
        return 'friendly cartoon animal'
    
    def retry_with_fallback(self, original_prompt: str) -> Dict[str, Any]:
        """
        Retry image generation with a fallback prompt
        
        Args:
            original_prompt: Original prompt that failed
            
        Returns:
            Dict containing retry results
        """
        fallback_prompt = self._get_fallback_prompt(original_prompt)
        
        self.logger.info(f"Retrying with fallback prompt: {fallback_prompt}")
        
        return self.generate_coloring_sheet(fallback_prompt, confidence=0.6) 