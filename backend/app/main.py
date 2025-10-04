from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title= "Hackathon")

# Adding the Cors MiddleWare
app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"]
)


