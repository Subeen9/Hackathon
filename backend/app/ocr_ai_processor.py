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
gemini_model = genai.GenerativeModel('gemini-2.5-pro')

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
    
def accuracy_improvement_with_gemini(raw_text: str) -> str:
    """
    Using Gemini to correct and improve Latin text
    """
    prompt=f"""You are a Latin paleography expert. The text below is OCR output from a medieval Latin manuscript with many errors.

Your task:

Correct OCR mistakes (e.g. wrong/missing letters, merged words)

Add proper spaces between words

Remove strange symbols (e.g. ɲ, Č, ő, *, etc.)

Expand obvious abbreviations

Keep everything in Latin (no translation)

Preserve line breaks

RAW OCR TEXT:
{raw_text}"""

    try:
        print("=" * 60)
        print("CALLING GEMINI API")
        print("=" * 60)
        
        response = gemini_model.generate_content(prompt)
        
        print("GEMINI RESPONSE:")
        print(response.text)
        print("=" * 60)
        
        return response.text.strip()
        
    except Exception as e:
        print("=" * 60)
        print(f"GEMINI ERROR: {type(e).__name__}")
        print(f"ERROR MESSAGE: {str(e)}")
        print("=" * 60)
        return raw_text