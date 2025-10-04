from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
from fastapi.responses import FileResponse

router = APIRouter()
Upload_Dir = Path("uploads")
Upload_Dir.mkdir(exist_ok=True)

@router.get("/files/{filename}")
async def get_file(filename: str):
    file_path = Upload_Dir / filename
    if not file_path.exists():
        return {"error": "File not found"}
    return FileResponse(file_path)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = Upload_Dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "url": f"http://localhost:8000/files/{file.filename}"}


