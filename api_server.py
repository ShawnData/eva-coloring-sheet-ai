#!/usr/bin/env python3
"""
FastAPI server for Eva's Coloring Sheet AI
Handles voice processing requests from the React frontend
"""

import os
import tempfile
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv
from src.crews.coloring_sheet_crew import ColoringSheetCrew
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
ai_crew = ColoringSheetCrew()
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
            # Process with AI crew
            response = ai_crew.process_voice_input(transcription)
            # Generate TTS for the assistant's response
            tts_path = audio_utils.generate_tts(response.get('message', ''))
            tts_filename = os.path.basename(tts_path)
            tts_url = f"/api/tts/{tts_filename}"
            if response:
                return {
                    'transcription': transcription,
                    'message': response.get('message', 'I understand you!'),
                    'image_url': response.get('image_url', None),
                    'tts_url': tts_url
                }
            else:
                raise HTTPException(status_code=500, detail='Sorry, I couldn\'t generate a response. Please try again.')
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