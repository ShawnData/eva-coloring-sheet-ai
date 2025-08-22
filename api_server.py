#!/usr/bin/env python3
"""
FastAPI server for Eva's Coloring Sheet AI
Handles voice processing requests from the React frontend with multi-turn conversation support
"""

import os
import tempfile
import json
import uuid
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv
from src.crews.coloring_sheet_crew import create_coloring_sheet_crew, process_conversation_turn
from src.utils.conversation_utils import ConversationManager, ConversationState
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
conversation_manager = ConversationManager()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
openai_client = openai.OpenAI(api_key=api_key)

@app.post("/api/process-voice")
async def process_voice(
    audio: UploadFile = File(...),
    session_id: str = "1" # Quick fix
):
    """Process voice input and return response with image and TTS audio"""
    try:
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get or create conversation session
        conversation_state = conversation_manager.get_session(session_id)
        if not conversation_state:
            conversation_state = conversation_manager.create_session(session_id)
        
        # Save the uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Transcribe the audio
            transcription = audio_utils.transcribe_audio(temp_path, openai_client)
            
            # Process the conversation turn
            result = process_conversation_turn(crew, transcription, conversation_state)
            
            # Update the conversation session
            conversation_manager.update_session(session_id, result["conversation_state"])
            
            # Extract response components
            message = result["message"]
            should_generate_image = result["should_generate_image"]
            error = result.get("error")
            image_url = result.get("image_url")
            
            # Generate image if requested
            if should_generate_image and not error:
                try:
                    # Create a separate crew for image generation
                    image_crew = create_coloring_sheet_crew()
                    image_inputs = {
                        "conversation_state": json.dumps(result["conversation_state"].to_dict())
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
                            if image_result.get("message"):
                                message = image_result["message"]
                        except json.JSONDecodeError:
                            error = "Failed to parse image generation result"
                except Exception as e:
                    error = f"Failed to generate image: {str(e)}"
            
            # Generate TTS for the assistant's response
            tts_path = audio_utils.generate_tts(message)
            tts_filename = os.path.basename(tts_path)
            tts_url = f"/api/tts/{tts_filename}"
            
            return {
                'session_id': session_id,
                'transcription': transcription,
                'message': message,
                'image_url': image_url,
                'tts_url': tts_url,
                'error': error,
                'conversation_state': result["conversation_state"].to_dict(),
                'should_generate_image': should_generate_image
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        print(f"Error processing voice input: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing voice input: {str(e)}")

@app.post("/api/reset-conversation")
async def reset_conversation(session_id: str):
    """Reset a conversation session"""
    try:
        conversation_state = conversation_manager.reset_session(session_id)
        if conversation_state:
            return {
                'session_id': session_id,
                'message': 'Conversation reset successfully',
                'conversation_state': conversation_state.to_dict()
            }
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        print(f"Error resetting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error resetting conversation: {str(e)}")

@app.get("/api/conversation/{session_id}")
async def get_conversation(session_id: str):
    """Get the current state of a conversation session"""
    try:
        conversation_state = conversation_manager.get_session(session_id)
        if conversation_state:
            return {
                'session_id': session_id,
                'conversation_state': conversation_state.to_dict()
            }
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        print(f"Error getting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting conversation: {str(e)}")

@app.delete("/api/conversation/{session_id}")
async def delete_conversation(session_id: str):
    """Delete a conversation session"""
    try:
        conversation_manager.delete_session(session_id)
        return {
            'session_id': session_id,
            'message': 'Conversation deleted successfully'
        }
    except Exception as e:
        print(f"Error deleting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

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