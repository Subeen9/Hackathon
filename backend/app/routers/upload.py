from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import os
from app.preprocess import preprocess_image
from app.ocr_ai_processor import extract_text_with_vision, accuracy_improvement_with_gemini
from fastapi.responses import FileResponse

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
        # Save original file
        original_file_path = UPLOAD_DIR / file.filename
        with open(original_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        ext = original_file_path.suffix.lower()
        
        if ext in [".jpg", ".jpeg", ".png"]:
            # Preprocess and save the preprocessed version
            preprocessed_path = preprocess_image(str(original_file_path))
            
            # Make sure preprocessed file is in uploads folder
            preprocessed_filename = f"preprocessed_{file.filename}"
            final_preprocessed_path = UPLOAD_DIR / preprocessed_filename
            
            # Copy preprocessed image to uploads folder if it's not already there
            if preprocessed_path != str(final_preprocessed_path):
                shutil.copy(preprocessed_path, final_preprocessed_path)
            
            # Use preprocessed version for OCR
            raw_text = extract_text_with_vision(str(final_preprocessed_path))
        else:
            # For PDFs, no preprocessing needed
            raw_text = extract_text_with_vision(str(original_file_path))

        # Improve text with Gemini
        accurate_text_gemini = accuracy_improvement_with_gemini(raw_text)

        # Return original file URL (user sees the original)
        # But we've saved the preprocessed one too
        return JSONResponse(content={
            "success": True,
            "original_filename": file.filename,
            "file_url": f"/api/files/{file.filename}",  # Show original
            "preprocessed_file": f"/api/files/preprocessed_{file.filename}" if ext in [".jpg", ".jpeg", ".png"] else None,  # Optional: frontend can access this too
            "raw_ocr_text": raw_text,
            "accurate_text": accurate_text_gemini,
            "message": "Vision + Gemini processing complete"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})