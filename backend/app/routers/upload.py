from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import os
from app.preprocess import preprocess_image
from app.ocr_ai_processor import extract_text_with_vision

router = APIRouter(prefix="/api", tags=["Upload & Preprocess"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.get("/files/{filename}")
async def get_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        return {"error": "File not found"}
    return FileResponse(file_path)

@router.post("/upload")
async def upload_and_preprocess(file: UploadFile = File(...)):
    """
    Upload an image or PDF, preprocess if image, extract text, improve with Gemini.
    Save both original and preprocessed, but show original to user.
    """
    try:
        
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        preprocessed_path = preprocess_image(str(file_path))
        # Extracting text using Google Vision
        raw_text = extract_text_with_vision(preprocessed_path)
        
        return JSONResponse(content={
            "success": True,
            "original_filename": file.filename,
            "raw_ocr_text": raw_text,
            "message": "Visoin is working"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})