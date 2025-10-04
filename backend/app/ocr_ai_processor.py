import os
import io
from google.cloud import vision
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# setting up Google Vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
vision_client = vision.ImageAnnotatorClient()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

def extract_text_with_vision(image_path: str) -> str:

# reading text from image with google vision api

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    
    if response.error.message:
        raise Exception(f'Vision API Error: {response.error.message}')
    
    texts = response.text_annotations
    if texts:
        return texts[0].description
    else:
        return "No text found"