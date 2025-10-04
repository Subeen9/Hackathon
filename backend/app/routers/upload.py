from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import shutil
from app.preprocess import preprocess_image  

router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_and_preprocess(file: UploadFile = File(...)):
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run preprocessing
        output_path = preprocess_image(str(file_path))

        return FileResponse(
            output_path,
            media_type="image/png",
            filename="preprocessed_clean.png"
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
