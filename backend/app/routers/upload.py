from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import shutil
import os
from pydantic import BaseModel
from app.preprocess import preprocess_image
from app.ocr_ai_processor import extract_text_with_vision
from app.textProcessor import get_text_processor
from app.textProcessor import clean_text

router = APIRouter(prefix="/api", tags=["Upload & Preprocess"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Pydantic model for text analysis requests
class TextAnalysisRequest(BaseModel):
    text: str
    language: str = "lat"

@router.get("/files/{filename}")
async def get_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(file_path)

@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    processor = get_text_processor()
    return JSONResponse(content={
        "languages": processor.get_supported_languages()
    })

@router.post("/upload")
async def upload_and_preprocess(
    file: UploadFile = File(...),
    language: str = "lat"
):
    """
    Upload, OCR, and analyze text in specified language
    """
    try:
        # Save original file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        ext = file_path.suffix.lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            preprocessed_path = preprocess_image(str(file_path))
        else:
            preprocessed_path = str(file_path)
        
        # Extract text using Google Vision
        raw_text = extract_text_with_vision(preprocessed_path)

        # Clean text
        accurate_text = clean_text(raw_text)
        
        # Analyze text
        processor = get_text_processor()
        if not language or language == "auto":
            language = processor.detect_language(raw_text)
        
        text_analysis = processor.analyze_text(raw_text, language)
        
        
        return JSONResponse(content={
            "success": True,
            "original_filename": file.filename,
            "file_url": f"/api/files/{file.filename}",
            "accurate_text":accurate_text,
            "raw_ocr_text": raw_text,
            "text_analysis": text_analysis,
            "detected_language": language,
            "message": "OCR and linguistic analysis complete"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/analyze-text")
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text on-demand with specified language
    Useful for when user corrects OCR text and wants to re-analyze
    """
    try:
        processor = get_text_processor()
        analysis = processor.analyze_text(request.text, request.language)
        return JSONResponse(content=analysis)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})