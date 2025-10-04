import os
import io
from google.cloud import vision
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Google Vision setup
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
vision_client = vision.ImageAnnotatorClient()

# Gemini setup
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Find available models
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

def correct_old_english_with_gemini(raw_text: str) -> str:
    prompt = f"""You are an expert in Old English (Anglo-Saxon) paleography and manuscript transcription.

I have OCR output from an Old English manuscript with errors. Correct it:

1. Fix OCR mistakes (wrong letters, merged words, gibberish)
2. Add proper word boundaries
3. Preserve Old English special characters: þ (thorn), ð (eth), æ (ash), ƿ (wynn)
4. Expand common Old English abbreviations (þ̄→þæt, ⁊→and, 7→and)
5. Keep in Old English - DO NOT translate to Modern English
6. Remove symbols/asterisks/gibberish that are clearly OCR errors
7. Format with line breaks
8. Maintain authentic Anglo-Saxon spelling

RAW OCR:
{raw_text}

Return ONLY corrected Old English text:"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        return raw_text

def correct_sanskrit_with_gemini(raw_text: str) -> str:
    prompt = f"""You are an expert in Sanskrit paleography and manuscript transcription, specializing in Devanagari script.

I have OCR output from a Sanskrit manuscript with errors. Correct it:

1. Fix OCR mistakes (wrong letters, merged words, misread characters)
2. Add proper word boundaries (respect Sanskrit sandhi rules)
3. Preserve Devanagari characters correctly: क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श ष स ह
4. Preserve vowel marks (diacritics): ा ि ी ु ू ृ ॄ ॢ े ै ो ौ ं ः ँ
5. Expand common Sanskrit abbreviations if present
6. Keep in Sanskrit Devanagari script - DO NOT transliterate or translate
7. Remove symbols/asterisks/gibberish that are clearly OCR errors
8. Format with proper line breaks
9. Maintain authentic Sanskrit orthography

RAW OCR:
{raw_text}

Return ONLY corrected Sanskrit text in Devanagari script:"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        return raw_text

def correct_greek_with_gemini(raw_text: str) -> str:
    prompt = f"""You are an expert in Ancient Greek paleography and manuscript transcription.

I have OCR output from an Ancient Greek manuscript with errors. Correct it:

1. Fix OCR mistakes (wrong letters, merged words, misread characters)
2. Add proper word boundaries
3. Preserve Greek alphabet correctly: Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω
4. Preserve lowercase: α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ ς τ υ φ χ ψ ω
5. Preserve diacritical marks (accents and breathing marks): ά έ ή ί ό ύ ώ ὰ ὲ ὴ ὶ ὸ ὺ ὼ ἀ ἁ ἐ ἑ ἠ ἡ ἰ ἱ ὀ ὁ ὐ ὑ ὠ ὡ
6. Expand common Greek abbreviations (nomina sacra: ΘΣ→ΘΕΟΣ, ΙΣ→ΙΗΣΟΥΣ, ΧΣ→ΧΡΙΣΤΟΣ)
7. Keep in Ancient Greek - DO NOT translate
8. Remove symbols/asterisks/gibberish that are clearly OCR errors
9. Format with proper line breaks
10. Maintain authentic Ancient Greek orthography

RAW OCR:
{raw_text}

Return ONLY corrected Ancient Greek text:"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        return raw_text
    
def correct_text_with_gemini(raw_text: str, language: str) -> str:
    """
    Router function that picks the right correction function based on language
    """
    if language == "latin":
        return correct_latin_with_gemini(raw_text)
    elif language == "old_english":
        return correct_old_english_with_gemini(raw_text)
    elif language == "sanskrit":
        return correct_sanskrit_with_gemini(raw_text)
    elif language == "greek":
        return correct_greek_with_gemini(raw_text)
    else:
        # Fallback to raw text if language not supported yet
        return raw_text