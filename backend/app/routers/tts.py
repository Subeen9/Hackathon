from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.cloud import texttospeech
from google.oauth2 import service_account
import base64

router = APIRouter()

class TTSRequest(BaseModel):
    text: str

@router.post("/tts")
async def text_to_speech(request: TTSRequest):
    try:
        # Load credentials from another service account
        credentials = service_account.Credentials.from_service_account_file("credentials2.json")
        client = texttospeech.TextToSpeechClient(credentials=credentials)

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

        audio_base64 = base64.b64encode(response.audio_content).decode("utf-8")
        return {"audio": audio_base64}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
