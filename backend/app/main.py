from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload
# Removed: from app.preprocess import preprocess_image
# Removed: from fastapi import UploadFile, File
# Removed: from fastapi.responses import FileResponse, JSONResponse
import os

app = FastAPI(title="Hackathon")

# Enable CORS
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

# Removed the entire @app.post("/preprocess") function to resolve the circular import