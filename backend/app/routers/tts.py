# backend/api/tts.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.cloud import texttospeech
import base64

router = APIRouter()

class TTSRequest(BaseModel):
    text: str

@router.post("/tts")
async def text_to_speech(request: TTSRequest):
    try:
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=request.text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Standard-C"
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # Return as base64 so frontend can play it directly
        audio_base64 = base64.b64encode(response.audio_content).decode("utf-8")
        return {"audio": audio_base64}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
