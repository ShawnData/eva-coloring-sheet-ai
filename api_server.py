#!/usr/bin/env python3
"""
FastAPI server for Eva's Coloring Sheet AI
Handles voice processing requests from the React frontend
"""

import os
import tempfile
import json
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv
from src.crews.coloring_sheet_crew import create_coloring_sheet_crew
from src.utils.audio_utils import AudioUtils
import openai
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
crew = create_coloring_sheet_crew()
audio_utils = AudioUtils()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
openai_client = openai.OpenAI(api_key=api_key)

@app.post("/api/process-voice")
async def process_voice(audio: UploadFile = File(...)):
    """Process voice input and return response with image and TTS audio"""
    try:
        # Save the uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_path = temp_file.name
        try:
            # Transcribe the audio
            transcription = audio_utils.transcribe_audio(temp_path, openai_client)
            # Run CrewAI workflow
            crew_output = crew.kickoff(inputs={"voice_input": transcription})
            result = crew_output.to_dict()
            print(f"Crew output: {result}")
            
            # Extract the final result from the crew output
            # The crew output has the result in the raw attribute as a JSON string
            if hasattr(crew_output, 'raw') and crew_output.raw:
                try:
                    # Remove the ```json and ``` markers if present
                    raw_str = crew_output.raw.strip()
                    if raw_str.startswith('```json'):
                        raw_str = raw_str[7:]  # Remove ```json
                    if raw_str.endswith('```'):
                        raw_str = raw_str[:-3]  # Remove ```
                    
                    final_output = json.loads(raw_str.strip())
                except json.JSONDecodeError:
                    final_output = {"message": crew_output.raw, "image_url": None, "error": "Failed to parse output"}
            else:
                # Fallback: try to_dict() method
                result = crew_output.to_dict()
                
                if isinstance(result, dict) and 'tasks_outputs' in result:
                    # Get the output from the last task (designer agent)
                    task_outputs = result['tasks_outputs']
                    if task_outputs and len(task_outputs) > 0:
                        final_output = task_outputs[-1]  # Last task output
                        if isinstance(final_output, str):
                            try:
                                final_output = json.loads(final_output)
                            except json.JSONDecodeError:
                                final_output = {"message": final_output, "image_url": None, "error": "Failed to parse output"}
                        elif not isinstance(final_output, dict):
                            final_output = {"message": str(final_output), "image_url": None, "error": None}
                    else:
                        final_output = {"message": "No output generated", "image_url": None, "error": "No task output"}
                else:
                    # Fallback: try to extract from the result directly
                    final_output = result if isinstance(result, dict) else {"message": str(result), "image_url": None, "error": None}
            
            # Extract message and image_url from the final output
            message = final_output.get("message", "I'm sorry, I couldn't process your request.")
            image_url = final_output.get("image_url")
            error = final_output.get("error")
            
            # Generate TTS for the assistant's response
            tts_path = audio_utils.generate_tts(message)
            tts_filename = os.path.basename(tts_path)
            tts_url = f"/api/tts/{tts_filename}"
            
            return {
                'transcription': transcription,
                'message': message,
                'image_url': image_url,
                'tts_url': tts_url,
                'error': error
            }
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    except Exception as e:
        print(f"Error processing voice input: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing voice input: {str(e)}")

@app.get("/api/tts/{filename}")
async def get_tts_file(filename: str):
    """Serve generated TTS audio files"""
    tts_dir = audio_utils.temp_tts_dir
    file_path = tts_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="TTS file not found")
    return FileResponse(str(file_path), media_type="audio/mpeg")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': "Eva's Coloring Sheet AI is running!"}

if __name__ == '__main__':
    print("🎨 Starting Eva's Coloring Sheet AI API Server...")
    print("📡 API will be available at: http://localhost:5000")
    print("🌐 React frontend should connect to: http://localhost:3000")
    uvicorn.run("api_server:app", host="0.0.0.0", port=5000, reload=True) 