from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import shutil
import os
from app.preprocess import preprocess_image
from app.ocr_ai_processor import extract_text_with_vision, accuracy_improvement_with_gemini

router = APIRouter(prefix="/api", tags=["Upload & Preprocess"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_and_preprocess(file: UploadFile = File(...)):
    """
    Upload an image file, preprocess it, and use google vision to extract text.
    """
    try:
        
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        preprocessed_path = preprocess_image(str(file_path))
        # Extracting text using Google Vision
        raw_text = extract_text_with_vision(preprocessed_path)
        
        # Accuracy improvement with Gemini
        accurate_text_gemini = accuracy_improvement_with_gemini(raw_text)
        
        
        return JSONResponse(content={
            "success": True,
            "original_filename": file.filename,
            "preprocessed_image": "preprocessed_clean.png",
            "raw_ocr_text": raw_text,
            "accurate_text": accurate_text_gemini,
            "message": "vision and gemini working"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})