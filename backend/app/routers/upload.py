from fastapi import APIRouter, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse, FileResponse 
from pathlib import Path
import shutil
from pydantic import BaseModel
from app.preprocess import preprocess_image
from app.ocr_ai_processor import extract_text_with_vision, correct_text_with_ollama
from deep_translator import GoogleTranslator
from app.textProcessor import get_text_processor

router = APIRouter(prefix="/api", tags=["Upload & Preprocess"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
LANGUAGE_MAP = {
    "latin": "lat",
    "lat": "lat",
    "ancient greek": "grc",
    "greek": "grc",
    "old english": "ang",
    "english": "ang"
}

def normalize_language(lang: str) -> str:
    lang = lang.strip().lower()
    return LANGUAGE_MAP.get(lang, "lat")

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

@router.post("/files/translation")
async def translate_text(
    text: str = Body(..., embed=True),
    source_lang: str = Body("auto"),
    target_lang: str = Body("en")
):
    if not text.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Text cannot be empty"}
        )
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    translated_text = translator.translate(text)
    return JSONResponse(content={
        "success": True,
        "message": f"Translated from {source_lang} to {target_lang}",
        "original_text": text,
        "translated_text": translated_text,
        "source_lang": source_lang,
        "target_lang": target_lang
    })

@router.post("/upload")
async def upload_and_preprocess(
    file: UploadFile = File(...),
    language: str = Form("lat")
):
    """
    Upload an image or PDF, preprocess if image, extract text, and analyze.
    Languages: lat (Latin), grc (Greek), ang (Old English)
    """
    try:
        # Save original file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Preprocess images
        ext = file_path.suffix.lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            preprocessed_path = preprocess_image(str(file_path))
        else:
            preprocessed_path = str(file_path)
        
        # Extract text using Google Vision
        raw_text = extract_text_with_vision(preprocessed_path)
        
        # Correct text with Gemini (clean up OCR errors)
        corrected_text = correct_text_with_ollama(raw_text, language)
        
        # Analyze corrected text with CLTK for lemmas/POS
        processor = get_text_processor()
        
        # Auto-detect language if needed
        if not language or language == "auto":
            language = processor.detect_language(corrected_text)
        
        # Get linguistic analysis (lemma + POS)
        language = normalize_language(language)
        try:
           text_analysis = processor.analyze_text(corrected_text, language)
        except Exception as e:
            print(f" Text analysis failed for {language}: {e}")
            text_analysis = None 
        

        
        return JSONResponse(content={
            "success": True,
            "language": language,
            "original_filename": file.filename,
            "file_url": f"/api/files/{file.filename}",
            "preprocessed_file": f"/api/files/preprocessed_clean.png" if ext in [".jpg", ".jpeg", ".png"] else None,
            "raw_ocr_text": raw_text,
            "accurate_text": corrected_text,
            "text_analysis": text_analysis,
            "detected_language": language,
            "message": "OCR and linguistic analysis complete"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()  # Print full error for debugging
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/analyze-text")
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text on-demand with specified language.
    Useful when user corrects OCR text and wants to re-analyze.
    """
    try:
        processor = get_text_processor()
        analysis = processor.analyze_text(request.text, request.language)
        return JSONResponse(content={
            "success": True,
            "text_analysis": analysis,
            "language": request.language
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})