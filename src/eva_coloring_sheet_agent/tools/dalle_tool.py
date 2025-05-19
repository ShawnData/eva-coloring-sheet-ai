from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import yaml
from openai import OpenAI
from pathlib import Path
import webbrowser

#class DALLEImageGeneratorInput(BaseModel):
    #"""Input schema for DALLEImageGenerator."""
    #prompt: str = Field(..., description="The detailed description of the coloring page to generate")

class DALLEImageGenerator(BaseTool):
    name: str = "DALL-E Image Generator"
    description: str = (
        "A tool that generates coloring page images using DALL-E based on detailed descriptions. "
        "It creates high-quality, black-and-white outline images suitable for coloring."
    )
    #args_schema: Type[BaseModel] = DALLEImageGeneratorInput

    def __init__(self, config_path: str = "src/eva_coloring_sheet_agent/config/settings.yaml"):
        super().__init__()
        self._config_path = config_path
        self._config = self._load_config()
        self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def _load_config(self) -> dict:
        with open(self._config_path, 'r') as f:
            return yaml.safe_load(f)['dalle_image_generator']
    
    def _run(self, prompt: str) -> str:
        """
        Generate an image using DALL-E based on the provided prompt.
        
        Args:
            prompt (str): The description of the image to generate
            
        Returns:
            str: URL to the image if successful, error message if failed
        """
        try:
            # Generate image using DALL-E
            response = self._client.images.generate(
                model=self._config['model'],
                prompt=prompt,
                size=self._config['size'],
                quality=self._config['quality'],
                style=self._config['style'],
                n=self._config['n'],
                response_format=self._config['response_format'],
            )
            
            image_url = response.data[0].url
            print(f"Image URL: {image_url}")
            
            # Open the image URL in the default browser
            try:
                webbrowser.open(image_url)
            except webbrowser.Error:
                print("Error opening the image URL in the default browser.")
            
            return image_url
            
        except Exception as e:
            return f"Error generating image: {str(e)}" 