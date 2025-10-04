from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload
from app.preprocess import preprocess_image

from fastapi import UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import os

app = FastAPI(title="Hackathon")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Hackathon API is running 🚀"}

app.include_router(upload.router)



@app.post("/preprocess")
async def preprocess_file(file: UploadFile = File(...)):
    try:
     
        input_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(input_path, "wb") as f:
            f.write(await file.read())

   
        output_path = preprocess_image(input_path)

        return FileResponse(
            output_path,
            media_type="image/png",
            filename="preprocessed_clean.png"
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
