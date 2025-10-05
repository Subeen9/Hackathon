import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        """Initialize minimal CLTK processors for supported languages."""
        self.processors: Dict[str, object] = {}
        self.supported_languages = {
            "lat": "Latin",
            "grc": "Ancient Greek",
            "ang": "Old English",
        }
        logger.info("TextProcessor initialized.")

    def _load_processor(self, language_code: str):
        """Lazy-load CLTK NLP processor for the given language."""
        if language_code not in self.supported_languages:
            logger.error(f"Unsupported language: {language_code}")
            return None

        if language_code not in self.processors:
            try:
                from cltk import NLP
                logger.info(f"Loading CLTK pipeline for {self.supported_languages[language_code]}...")
                nlp = NLP(language_code, suppress_banner=True)
                _ = nlp.pipeline.processes  # Ensure pipeline built
                self.processors[language_code] = nlp
                logger.info(f"Successfully loaded {language_code} NLP pipeline.")
            except Exception as e:
                logger.exception(f"Failed to load CLTK for {language_code}: {e}")
                return None

        return self.processors[language_code]

    def analyze_text(self, text: str, language: str = "lat") -> List[Dict]:
        """Analyze text and return word, lemma, and POS only."""
        if language not in self.supported_languages:
            return [{"error": f"Language '{language}' not supported"}]

        nlp = self._load_processor(language)
        if not nlp:
            return [{"error": f"Failed to load NLP pipeline for '{language}'"}]

        try:
            doc = nlp.analyze(text)
            results = []
            for word in getattr(doc, "words", []):
                if not getattr(word, "lemma", None):
                    continue
                pos = getattr(word, "pos", "UNKNOWN")
                if pos in {"PUNCT", "X"}:
                    continue
                results.append({
                    "word": word.string,
                    "lemma": word.lemma,
                    "pos": self._get_pos_description(pos)
                })
            return results
        except Exception as e:
            logger.exception(f"Error analyzing text for {language}: {e}")
            return [{"error": str(e)}]

    def _get_pos_description(self, pos: str) -> str:
        """Readable POS mapping."""
        pos_map = {
            "NOUN": "noun", "VERB": "verb", "ADJ": "adjective", "ADV": "adverb",
            "PRON": "pronoun", "ADP": "preposition", "CONJ": "conjunction",
            "CCONJ": "conjunction", "DET": "determiner", "NUM": "numeral",
            "PART": "particle", "PROPN": "proper_noun",
        }
        return pos_map.get(pos, pos.lower())

    def detect_language(self, text: str) -> str:
        """Simple heuristic language detector."""
        t = text.lower()
        if any(w in t for w in ["et", "est", "sum", "sunt", "sed", "enim"]):
            return "lat"
        if any(w in t for w in ["kai", "ho", "tou", "te", "en"]):
            return "grc"
        if any(w in t for w in ["þæt", "and", "se", "heo", "his"]):
            return "ang"
        return "lat"

    def get_supported_languages(self) -> Dict[str, str]:
        return self.supported_languages
    
    

# Singleton
_text_processor: TextProcessor | None = None

def get_text_processor():
    global _text_processor
    if _text_processor is None:
        _text_processor = TextProcessor()
    return _text_processor

def clean_text(text: str) -> str:
        """
    Clean OCR text for frontend display:
    - Remove strange symbols or artifacts
    - Collapse multiple spaces
    - Normalize line breaks
        """
    # Remove non-printable characters (keep basic punctuation)
        text = re.sub(r"[^\w\s.,;:!?()'-]", " ", text)
    
    # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)
    
    # Optional: split into sentences/lines for readability
        text = re.sub(r"\s*([.;!?])\s*", r"\1\n", text)
    
        return text.strip()
