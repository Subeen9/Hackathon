import os
import io
from google.cloud import vision
import google.generativeai as genai
from dotenv import load_dotenv
import requests

load_dotenv()

# Google Vision setup
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
vision_client = vision.ImageAnnotatorClient()

# Ollama setup
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1" #This will default model but qwen will be used for non Latin languages

def call_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    """
    Call Ollama API with a prompt and return the response
    """
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower for more deterministic corrections
                "top_p": 0.9,
                "num_predict": 2000  
            }
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        raw_response = result.get("response", "").strip()
        
        # Clean up common LLM preambles and postscripts
        cleaned = clean_llm_response(raw_response)
        return cleaned
    
    except requests.exceptions.RequestException as e:
        print(f"Ollama API error: {e}")
        return ""

def clean_llm_response(text: str) -> str:
    """
    Remove common LLM conversational wrappers and return just the content
    """
    # Common phrases to remove
    unwanted_phrases = [
        "Here is the corrected",
        "Here's the corrected",
        "The corrected text is:",
        "CORRECTED TEXT:",
        "Return ONLY corrected",
        "Note:",
        "I've kept the formatting",
        "I have corrected",
        "Below is the corrected",
        "Here is your corrected"
    ]
    
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip lines that contain unwanted phrases (case insensitive)
        if any(phrase.lower() in line.lower() for phrase in unwanted_phrases):
            continue
        # Skip lines that are just explanations or meta-commentary
        if line.strip().startswith("Note:") or line.strip().startswith("I've"):
            continue
        cleaned_lines.append(line)
    
    result = '\n'.join(cleaned_lines).strip()
    
    # Remove any leading/trailing markdown code blocks if present
    if result.startswith("```") and result.endswith("```"):
        lines = result.split('\n')
        result = '\n'.join(lines[1:-1]).strip()
    
    return result

def extract_text_with_vision(image_path: str) -> str:
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    
    if response.error.message:
        raise Exception(f'Vision API Error: {response.error.message}')
    
    texts = response.text_annotations
    return texts[0].description if texts else "No text found"

def correct_latin_with_ollama(raw_text: str) -> str:
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

CRITICAL: Return ONLY the corrected Latin text. No explanations, no "here is", no notes, no commentary. Just the text itself."""

    corrected = call_ollama(prompt)
    return corrected if corrected else raw_text

def correct_old_english_with_ollama(raw_text: str) -> str:
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

CRITICAL: Return ONLY the corrected Old English text. No explanations, no "here is", no notes, no commentary. Just the text itself."""

    corrected = call_ollama(prompt)
    return corrected if corrected else raw_text

def correct_sanskrit_with_ollama(raw_text: str) -> str:
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

CRITICAL: Return ONLY the corrected Sanskrit text in Devanagari script. No explanations, no "here is", no notes, no commentary. Just the text itself."""

    corrected = call_ollama(prompt, model="qwen2.5")  # Better for non-Latin scripts
    return corrected if corrected else raw_text

def correct_greek_with_ollama(raw_text: str) -> str:
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

CRITICAL: Return ONLY the corrected Ancient Greek text. No explanations, no "here is", no notes, no commentary. Just the text itself."""

    corrected = call_ollama(prompt, model="qwen2.5")  # Better for non-Latin scripts
    return corrected if corrected else raw_text
    
def correct_text_with_ollama(raw_text: str, language: str) -> str:
    """
    Router function that picks the right correction function based on language
    """
    if language == "latin":
        return correct_latin_with_ollama(raw_text)
    elif language == "old_english":
        return correct_old_english_with_ollama(raw_text)
    elif language == "sanskrit":
        return correct_sanskrit_with_ollama(raw_text)
    elif language == "greek":
        return correct_greek_with_ollama(raw_text)
    else:
        # Fallback to raw text if language not supported yet
        return raw_text