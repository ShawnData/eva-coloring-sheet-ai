import os
from crewai.tools import BaseTool
from typing import Optional, Literal
import openai

class ColoringSheetDalleTool(BaseTool):
    """Enhanced DALL-E tool specifically for generating child-appropriate coloring sheets"""
    name: str = "generate_coloring_sheet"
    description: str = "Generate a child-appropriate coloring sheet image using DALL-E 3"

    def __post_init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = "dall-e-3"
        self.size: Literal["1024x1024"] = "1024x1024"
        self.quality: Literal["standard"] = "standard"
        self.response_format: Literal["url"] = "url"
        self.n = 1
    
    def _run(self, prompt: str) -> str:
        """
        Generate a coloring sheet image using DALL-E 3
        
        Args:
            prompt: The description of what to create (e.g., "a happy cat")
            
        Returns:
            str: URL of the generated image
        """
        try:
            # Always initialize OpenAI client here
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise Exception("OPENAI_API_KEY environment variable is not set")
            client = openai.OpenAI(api_key=api_key)
            model = "dall-e-3"
            size = "1024x1024"
            quality = "standard"
            response_format = "url"
            n = 1
            # Enhance prompt for coloring sheet style
            enhanced_prompt = self._create_coloring_sheet_prompt(prompt)
            # Generate image using DALL-E
            response = client.images.generate(
                model=model,
                prompt=enhanced_prompt,
                size=size,
                quality=quality,
                response_format=response_format,
                n=n
            )
            # Ensure we return a string URL
            image_url = response.data[0].url
            if image_url is None:
                raise Exception("No image URL returned from DALL-E")
            return image_url
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")
    
    def _create_coloring_sheet_prompt(self, base_prompt: str) -> str:
        """
        Create a DALL-E prompt optimized for coloring sheets for 6-year-olds
        
        Args:
            base_prompt: The basic description from the child
            
        Returns:
            str: Enhanced prompt for DALL-E
        """
        # Clean and filter the base prompt for safety
        safe_prompt = self._filter_content(base_prompt)
        
        # Create coloring sheet specific prompt
        enhanced_prompt = f"""
        Create a black and white line art coloring sheet suitable for a 6-year-old child. 
        The image should be: {safe_prompt}
        
        Style requirements:
        - Simple, clear black lines on white background
        - Cartoon-style, friendly and appealing to children
        - Large, easy-to-color areas
        - No shading or complex details
        - Clean, bold outlines
        - Age-appropriate and safe content
        - High contrast for easy coloring
        
        The image should look like a traditional coloring book page that a 6-year-old would enjoy coloring.
        """
        
        return enhanced_prompt.strip()
    
    def _filter_content(self, prompt: str) -> str:
        """
        Filter content to ensure it's appropriate for 6-year-olds
        
        Args:
            prompt: Original prompt from child
            
        Returns:
            str: Filtered, safe prompt
        """
        # Convert to lowercase for easier filtering
        lower_prompt = prompt.lower()
        
        # List of inappropriate content to filter out
        inappropriate_words = [
            'violence', 'weapon', 'gun', 'knife', 'blood', 'death', 'scary',
            'monster', 'ghost', 'zombie', 'vampire', 'witch', 'evil', 'dark',
            'adult', 'sexy', 'nude', 'alcohol', 'drug', 'smoke'
        ]
        
        # Check for inappropriate content
        for word in inappropriate_words:
            if word in lower_prompt:
                # Replace with appropriate alternative
                if 'scary' in lower_prompt or 'monster' in lower_prompt:
                    return "a friendly, cute character"
                elif 'weapon' in lower_prompt or 'gun' in lower_prompt:
                    return "a fun toy or game"
                else:
                    return "a happy, friendly animal or character"
        
        # If prompt is too complex, simplify it
        if len(prompt.split()) > 10:
            # Take the first few words to keep it simple
            words = prompt.split()[:5]
            return " ".join(words)
        
        return prompt

# Create a global instance for easy access
dalle_tool = ColoringSheetDalleTool()