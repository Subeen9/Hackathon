from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse 
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
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(file_path)

@router.post("/upload")
async def upload_and_preprocess(file: UploadFile = File(...)):
    """
    Upload an image or PDF, preprocess if image, extract text.
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
        
        return JSONResponse(content={
            "success": True,
            "original_filename": file.filename,
            "file_url": f"/api/files/{file.filename}",
            "preprocessed_file": f"/api/files/preprocessed_{file.filename}" if ext in [".jpg", ".jpeg", ".png"] else None, 
            "raw_ocr_text": raw_text,
            "accurate_text": raw_text,  # Add this so frontend gets processedText
            "message": "Vision is working"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})