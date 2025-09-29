import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import requests

router = APIRouter(prefix="/speech", tags=["Speech-to-Text"])

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = "add key here"
OPENAI_AUDIO_URL = "https://api.openai.com/v1/audio/transcriptions"


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Upload an audio file (mp3, wav, m4a, etc.) and get the transcribed text.
    """
    try:
        # Save file temporarily
        file_bytes = await file.read()

        # Send to OpenAI Whisper API
        files = {
            "file": (file.filename, file_bytes, file.content_type),
        }
        data = {
            "model": "gpt-4o-mini-transcribe"   # Fast, accurate transcription model
        }
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        response = requests.post(OPENAI_AUDIO_URL, headers=headers, data=data, files=files)
        response_json = response.json()

        return JSONResponse(content={"transcription": response_json.get("text", "")})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
