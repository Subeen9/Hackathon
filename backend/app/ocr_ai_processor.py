import os
import io
from google.cloud import vision
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Google Vision setup
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
vision_client = vision.ImageAnnotatorClient()

# Gemini setup - match Colab approach
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Find available models like in Colab
available_models = []
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        available_models.append(m.name)

if available_models:
    model_name = available_models[0]
    print(f"Using Gemini model: {model_name}")
    gemini_model = genai.GenerativeModel(model_name)
else:
    raise Exception("No Gemini models available")

def extract_text_with_vision(image_path: str) -> str:
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    
    if response.error.message:
        raise Exception(f'Vision API Error: {response.error.message}')
    
    texts = response.text_annotations
    return texts[0].description if texts else "No text found"

def correct_latin_with_gemini(raw_text: str) -> str:
    prompt = f"""You are an expert in medieval Latin paleography and manuscript transcription.

I have OCR output from a medieval Latin manuscript (Vulgate Bible) with errors. Correct it:

1. Fix OCR mistakes (wrong letters, merged words, gibberish)
2. Add proper word boundaries
3. Expand abbreviations (DNS→DOMINUS, XPS→CHRISTUS)
4. Keep in Latin - DO NOT translate
5. Remove symbols/asterisks/gibberish
6. Format with line breaks

RAW OCR:
{raw_text}

Return ONLY corrected Latin text:"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        return raw_text