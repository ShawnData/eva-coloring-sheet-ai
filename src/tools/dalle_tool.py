import os
from crewai_tools import DallETool

dalle_tool = DallETool(model="dall-e-3",
                       size="1024x1024",
                       quality="standard",
                       response_format="url",
                       api_key=os.getenv("OPENAI_API_KEY"),
                       n=1)