from cltk import NLP
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        """Initialize NLP processors for multiple languages"""
        self.processors = {}
        self.supported_languages = {
            "lat": "Latin",
            "grc": "Ancient Greek",
            "ang": "Old English",
            "fro": "Old French",
            "got": "Gothic",
            "arb": "Arabic",
            "heb": "Hebrew"
        }
        logger.info("TextProcessor initialized")
    
    def _load_processor(self, language_code: str):
        """Lazy load language processor when needed"""
        if language_code not in self.processors:
            try:
                logger.info(f"Loading {self.supported_languages.get(language_code, language_code)} models...")
                self.processors[language_code] = NLP(language=language_code, suppress_banner=True)
                logger.info(f"{language_code} models loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load {language_code}: {e}")
                return None
        return self.processors[language_code]
    
    def analyze_text(self, text: str, language: str = "lat") -> Dict:
        """
        Analyze text in specified language and return word-level annotations
        
        Args:
            text: The text to analyze
            language: ISO 639-3 language code (lat, grc, ang, etc.)
        
        Returns:
            Dictionary with annotated_words, glossary, and stats
        """
        if language not in self.supported_languages:
            return {
                "error": f"Language '{language}' not supported",
                "supported_languages": self.supported_languages
            }
        
        nlp = self._load_processor(language)
        if not nlp:
            return {"error": f"Failed to load {language} processor"}
        
        try:
            doc = nlp.analyze(text=text)
            
            annotated_words = []
            glossary = {}
            
            for word in doc.words:
                if hasattr(word, 'lemma') and word.lemma:
                    pos = word.pos if hasattr(word, 'pos') else 'UNKNOWN'
                    
                    # Skip punctuation
                    if pos in ['PUNCT', 'X']:
                        continue
                    
                    word_info = {
                        "word": word.string,
                        "lemma": word.lemma,
                        "pos": pos,
                        "pos_description": self._get_pos_description(pos),
                        "language": language
                    }
                    
                    annotated_words.append(word_info)
                    
                    # Build glossary
                    word_lower = word.string.lower()
                    lemma_lower = word.lemma.lower()
                    
                    if word_lower != lemma_lower:
                        if lemma_lower not in glossary:
                            glossary[lemma_lower] = {
                                "lemma": word.lemma,
                                "pos": pos,
                                "pos_description": self._get_pos_description(pos),
                                "inflected_forms": []
                            }
                        if word.string not in glossary[lemma_lower]["inflected_forms"]:
                            glossary[lemma_lower]["inflected_forms"].append(word.string)
            
            return {
                "annotated_words": annotated_words,
                "glossary": glossary,
                "language": self.supported_languages[language],
                "language_code": language,
                "stats": {
                    "total_words": len(annotated_words),
                    "unique_lemmas": len(set(w["lemma"] for w in annotated_words))
                }
            }
        
        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
            return {"error": str(e)}
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Attempt to detect language (basic heuristic)
        You might want to use a proper language detection library
        """
        # Simple heuristic based on common words
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['et', 'est', 'sum', 'sunt', 'sed']):
            return "lat"
        elif any(word in text_lower for word in ['καὶ', 'τὸ', 'ὁ', 'τῆς']):
            return "grc"
        elif any(word in text_lower for word in ['and', 'the', 'þæt', 'on']):
            return "ang"
        
        # Default to Latin if unsure
        return "lat"
    
    def _get_pos_description(self, pos: str) -> str:
        """Convert POS tags to human-readable descriptions"""
        pos_map = {
            "NOUN": "noun",
            "VERB": "verb",
            "ADJ": "adjective",
            "ADV": "adverb",
            "PRON": "pronoun",
            "ADP": "preposition",
            "CONJ": "conjunction",
            "DET": "determiner",
            "NUM": "numeral",
            "PART": "particle",
            "PROPN": "proper noun"
        }
        return pos_map.get(pos, pos.lower())
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Return list of supported languages"""
        return self.supported_languages

# Singleton instance
_text_processor = None

def get_text_processor() -> TextProcessor:
    """Get or create text processor singleton"""
    global _text_processor
    if _text_processor is None:
        _text_processor = TextProcessor()
    return _text_processor