# src/document_processor.py
"""
Document processor for extracting text from astrology PDFs
"""

try:
     import PyPDF2
except ImportError:
    print("Installing PyPDF2...")
    import subprocess
    subprocess.check_call(["pip", "install", "PyPDF2"])
    import PyPDF2

import re
from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class ProcessedDocument:
    """Container for processed document data"""
    filename: str
    total_pages: int
    extracted_text: str
    sentences: List[str]
    astrological_sentences: List[str]


class DocumentProcessor:
    """
    Handles PDF text extraction and identification of astrological content
    """
    
    def __init__(self):
        # Common astrological terms for filtering content
        self.astro_keywords = {
            'planets': ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu'],
            'houses': ['house', '1st house', '2nd house', '3rd house', '4th house', '5th house', 
                      '6th house', '7th house', '8th house', '9th house', '10th house', '11th house', '12th house'],
            'signs': ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 
                     'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'],
            'effects': ['gives', 'causes', 'indicates', 'brings', 'results in', 'leads to', 'produces']
        }
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF using PyPDF2"""
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"Extracting text from: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            raise ValueError(f"Could not extract text from {pdf_path}: {e}")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Pre-processing: normalize characters and remove artifacts
        text = text.replace('�', '')
        text = re.sub(r'[\f\r]', '\n', text)
        text = re.sub(r'\n\d+\n', '\n', text)
        text = text.replace('\t', ' ')
        
        # Initial whitespace normalization
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common word combinations first
        common_combinations = {
            r'(?i)\bto\s*the\b': 'to the',
            r'(?i)\bin\s*the\b': 'in the',
            r'(?i)\bof\s*the\b': 'of the',
            r'(?i)\bby\s*the\b': 'by the',
            r'(?i)\bwith\s*the\b': 'with the',
            r'(?i)\bfrom\s*the\b': 'from the',
            r'(?i)\bglory\s*to\b': 'glory to',
            r'(?i)\bgives\s*up\b': 'gives up',
            r'(?i)\baspected\s*by\b': 'aspected by',
            r'(?i)\bplaced\s*in\b': 'placed in',
            r'(?i)\bresults\s*in\b': 'results in',
            r'(?i)\bleads\s*to\b': 'leads to',
            r'(?i)\bif\s*the\b': 'if the',
            r'(?i)\bthen\s*the\b': 'then the',
            r'(?i)\band\s*the\b': 'and the',
            r'(?i)\blike\s*the\b': 'like the'
        }
        
        for pattern, replacement in common_combinations.items():
            text = re.sub(pattern, replacement, text)
        
        # Split words aggressively
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # camelCase
        text = re.sub(r'([A-Za-z])([0-9])', r'\1 \2', text)  # letters and numbers
        text = re.sub(r'([0-9])([A-Za-z])', r'\1 \2', text)  # numbers and letters
        text = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', text)  # wordWord
        text = re.sub(r'([A-Z][a-z])([A-Z])', r'\1 \2', text)  # WordWORD
        
        # First pass: Fix verb-noun and noun-verb combinations
        verb_noun_patterns = [
            (r'(?i)Moonis', 'Moon is'),
            (r'(?i)Marsis', 'Mars is'),
            (r'(?i)Jupiteris', 'Jupiter is'),
            (r'(?i)Saturnis', 'Saturn is'),
            (r'(?i)should\s*be', 'should be'),
            (r'(?i)be\s*aspected', 'be aspected'),
            (r'(?i)produces\s*blood', 'produces blood'),
            (r'(?i)produces\s*bile', 'produces bile'),
            (r'(?i)gives\s*up', 'gives up'),
            (r'(?i)water\s*produces', 'water produces'),
            (r'(?i)fire\s*produces', 'fire produces')
        ]
        
        for pattern, replacement in verb_noun_patterns:
            text = re.sub(pattern, replacement, text)

        # Second pass: Fix common phrases and compounds
        phrase_patterns = [
            (r'(?i)Glory\s*to\s*the', 'Glory to the'),
            (r'(?i)whose\s*very\s*breathing', 'whose very breathing'),
            (r'(?i)this\s*world', 'this world'),
            (r'(?i)water\s*and', 'water and'),
            (r'(?i)blood\s*and', 'blood and'),
            (r'(?i)her\s*home', 'her home'),
            (r'(?i)that\s*time', 'that time'),
            (r'(?i)at\s*that', 'at that'),
            (r'(?i)in\s*upachaya', 'in upachaya'),
            (r'(?i)so\s*that\s*the', 'so that the'),
            (r'(?i)inter\s*course', 'intercourse')
        ]
        
        for pattern, replacement in phrase_patterns:
            text = re.sub(pattern, replacement, text)

        # Third pass: Fix word boundaries with common words
        boundary_patterns = [
            # Articles and determiners
            (r'(?i)\b(the|an?|this|that|these|those)([a-z])', r'\1 \2'),
            # Prepositions
            (r'(?i)\b(in|on|at|by|to|for|with|from|of|as)([a-z])', r'\1 \2'),
            # Conjunctions
            (r'(?i)\b(and|or|but|nor|yet|so|if|then|when|while|where)([a-z])', r'\1 \2'),
            # Verbs
            (r'(?i)\b(is|are|was|were|be|been|being|has|have|had)([a-z])', r'\1 \2'),
            (r'(?i)\b(do|does|did|will|would|shall|should|may|might|must)([a-z])', r'\1 \2'),
            (r'(?i)\b(gives|produces|causes|makes|brings|leads|results)([a-z])', r'\1 \2'),
            # Planets and signs
            (r'(?i)\b(sun|moon|mars|mercury|jupiter|venus|saturn|rahu|ketu)([a-z])', r'\1 \2'),
            # Astrological terms
            (r'(?i)\b(house|sign|aspect|planet|degree|conjunction|opposition|trine|square)([a-z])', r'\1 \2')
        ]
        
        for pattern, replacement in boundary_patterns:
            text = re.sub(pattern, replacement, text)

        # Fourth pass: Handle special cases
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # camelCase
        text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', text)  # ABCdef
        text = re.sub(r'([a-z])([0-9])', r'\1 \2', text)  # word123
        text = re.sub(r'([0-9])([a-z])', r'\1 \2', text)  # 123word

        # Final cleanup
        text = re.sub(r'\s+', ' ', text)  # normalize spaces
        text = text.strip()
        
        # Join single letters that should be together (like 's a' -> 'sa')
        text = re.sub(r'\b([A-Za-z])\s([A-Za-z])\b(?!\s*[A-Za-z])', r'\1\2', text)
        
        # Fix common astrological terms
        astro_terms = {
            'Sun': ['sun', 'sungod', 'sunis', 'sunin', 'surya'],
            'Moon': ['moon', 'moonis', 'moonin', 'chandra'],
            'Mars': ['mars', 'marsis', 'marsin', 'mangal', 'kuja'],
            'Mercury': ['mercury', 'mercuryis', 'mercuryin', 'budha'],
            'Jupiter': ['jupiter', 'jupiteris', 'jupiterin', 'guru', 'brihaspati'],
            'Venus': ['venus', 'venusis', 'venusin', 'shukra'],
            'Saturn': ['saturn', 'saturnis', 'saturnin', 'shani'],
            'Rahu': ['rahu', 'rahuis', 'rahuin'],
            'Ketu': ['ketu', 'ketuis', 'ketuin']
        }
        
        for proper, variants in astro_terms.items():
            pattern = f"(?i)({'|'.join(variants)})"
            text = re.sub(pattern, proper, text)
        
        # Fix common prepositions, articles and verbs
        common_words = [
            # Prepositions
            'in', 'of', 'with', 'by', 'at', 'on', 'to', 'for', 'from', 'into',
            # Articles
            'the', 'a', 'an',
            # Conjunctions
            'and', 'or', 'but', 'if', 'when', 'while', 'because', 'that',
            # Verbs
            'is', 'are', 'was', 'were', 'will', 'shall', 'has', 'have', 'had',
            'gives', 'causes', 'makes', 'brings', 'leads', 'results', 'produces',
            'indicates', 'signifies', 'denotes', 'shows', 'suggests'
        ]
        
        # Build pattern for word boundaries
        pattern = f"(?i)\\b({'|'.join(common_words)})\\b([a-z])"
        text = re.sub(pattern, r'\1 \2', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'([.,;!?])(?!\s)', r'\1 ', text)  # Add space after punctuation
        text = re.sub(r'\s+([.,;!?])', r'\1', text)  # Remove space before punctuation
        
        # Fix spacing around quotes and parentheses
        text = re.sub(r'(["\(])\s*', r'\1', text)
        text = re.sub(r'\s*(["\)])', r'\1', text)
        
        # Fix specific patterns
        text = re.sub(r'(?i)\b(to|in|of|by|with|from)the\b', r'\1 the', text)  # Fix merged articles
        text = re.sub(r'(?i)\b(gives|results|leads|placed|aspected)\s*(up|in|to|by)\b', r'\1 \2', text)  # Fix verb phrases
        
        # Final cleanup
        text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)  # Remove repeated words
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = text.strip()
        
        return text
    
    def chunk_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for easier processing"""
        sentences = re.split(r'[.!?]+', text)
        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if 10 <= len(sentence) <= 500:
                clean_sentences.append(sentence)
        return clean_sentences
    
    def contains_astrological_content(self, sentence: str) -> bool:
        """Check if a sentence contains astrological content"""
        sentence_lower = sentence.lower()
        
        # Check for planet + house combinations
        for planet in self.astro_keywords['planets']:
            if planet in sentence_lower:
                for house_term in self.astro_keywords['houses']:
                    if house_term in sentence_lower:
                        return True
        
        # Check for planet + sign combinations
        for planet in self.astro_keywords['planets']:
            if planet in sentence_lower:
                for sign in self.astro_keywords['signs']:
                    if sign in sentence_lower:
                        return True
        
        # Check for effect keywords
        for effect in self.astro_keywords['effects']:
            if effect in sentence_lower and any(planet in sentence_lower for planet in self.astro_keywords['planets']):
                return True
        
        return False
    
    def identify_astrological_content(self, sentences: List[str]) -> List[str]:
        """Filter sentences to keep only those with astrological content"""
        return [sentence for sentence in sentences if self.contains_astrological_content(sentence)]
    
    def process_document(self, pdf_path: str) -> ProcessedDocument:
        """Complete document processing pipeline"""
        print(f"Processing document: {pdf_path}")
        
        # Extract and clean text
        raw_text = self.extract_text(pdf_path)
        clean_text = self.clean_text(raw_text)
        
        # Split into sentences and find astrological content
        sentences = self.chunk_into_sentences(clean_text)
        astro_sentences = self.identify_astrological_content(sentences)
        
        filename = Path(pdf_path).name
        
        print(f"✅ Processed {filename}:")
        print(f"   Total sentences: {len(sentences)}")
        print(f"   Astrological sentences: {len(astro_sentences)}")
        
        return ProcessedDocument(
            filename=filename,
            total_pages=0,
            extracted_text=clean_text,
            sentences=sentences,
            astrological_sentences=astro_sentences
        )


# Test functionality
if __name__ == "__main__":
    print("Testing DocumentProcessor...")
    processor = DocumentProcessor()
    
    # Test astrological content detection
    test_sentences = [
        "Mars in the 7th house causes conflicts in marriage",
        "Jupiter gives wisdom when placed in its own sign",
        "This is just a regular sentence without astrology"
    ]
    
    for sentence in test_sentences:
        is_astro = processor.contains_astrological_content(sentence)
        print(f"'{sentence}' -> {is_astro}")





#     # Test PDF processing (replace with a valid PDF path)   
#     # pdf_path = "path/to/your/astrology_book.pdf"
#     # processed_doc = processor.process_document(pdf_path)
#     # print(f"Processed document: {processed_doc.filename}")
#     # print(f"Total pages: {processed_doc.total_pages}")# src/document_processor.py
# """
# Document processor for extracting text from astrology PDFs
# and identifying astrological content.
# """

# import PyPDF2
# import pdfplumber
# import re
# from typing import List, Optional
# from dataclasses import dataclass
# from pathlib import Path


# @dataclass
# class ProcessedDocument:
#     """Container for processed document data"""
#     filename: str
#     total_pages: int
#     extracted_text: str
#     sentences: List[str]
#     astrological_sentences: List[str]


# class DocumentProcessor:
#     """
#     Handles PDF text extraction and identification of astrological content
#     """
    
#     def __init__(self):
#         # Common astrological terms for filtering content
#         self.astro_keywords = {
#             'planets': ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu'],
#             'houses': ['house', '1st house', '2nd house', '3rd house', '4th house', '5th house', 
#                       '6th house', '7th house', '8th house', '9th house', '10th house', '11th house', '12th house'],
#             'signs': ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 
#                      'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'],
#             'effects': ['gives', 'causes', 'indicates', 'brings', 'results in', 'leads to', 'produces']
#         }
    
#     def extract_text_pypdf2(self, pdf_path: str) -> str:
#         """Extract text using PyPDF2 (fallback method)"""
#         try:
#             with open(pdf_path, 'rb') as file:
#                 pdf_reader = PyPDF2.PdfReader(file)
#                 text = ""
#                 for page in pdf_reader.pages:
#                     text += page.extract_text() + "\n"
#                 return text
#         except Exception as e:
#             print(f"PyPDF2 extraction failed: {e}")
#             return ""
    
#     def extract_text_pdfplumber(self, pdf_path: str) -> str:
#         """Extract text using pdfplumber (preferred method)"""
#         try:
#             text = ""
#             with pdfplumber.open(pdf_path) as pdf:
#                 for page in pdf.pages:
#                     page_text = page.extract_text()
#                     if page_text:
#                         text += page_text + "\n"
#             return text
#         except Exception as e:
#             print(f"pdfplumber extraction failed: {e}")
#             return ""
    
#     def extract_text(self, pdf_path: str) -> str:
#         """
#         Extract text from PDF using the best available method
#         """
#         if not Path(pdf_path).exists():
#             raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
#         print(f"Extracting text from: {pdf_path}")
        
#         # Try pdfplumber first (better for formatted text)
#         text = self.extract_text_pdfplumber(pdf_path)
        
#         # Fallback to PyPDF2 if pdfplumber fails
#         if not text.strip():
#             print("Trying PyPDF2 as fallback...")
#             text = self.extract_text_pypdf2(pdf_path)
        
#         if not text.strip():
#             raise ValueError(f"Could not extract text from {pdf_path}")
        
#         return text
    
#     def clean_text(self, text: str) -> str:
#         """Clean and normalize extracted text with enhanced classical text support"""
        
#         # Fix common PDF extraction issues for classical texts
#         # Fix broken planet names
#         text = re.sub(r'Mars\s*in', 'Mars in', text, flags=re.IGNORECASE)
#         text = re.sub(r'Jupiter\s*in', 'Jupiter in', text, flags=re.IGNORECASE)
#         text = re.sub(r'Venus\s*in', 'Venus in', text, flags=re.IGNORECASE)
#         text = re.sub(r'Saturn\s*in', 'Saturn in', text, flags=re.IGNORECASE)
#         text = re.sub(r'Sun\s*in', 'Sun in', text, flags=re.IGNORECASE)
#         text = re.sub(r'Moon\s*in', 'Moon in', text, flags=re.IGNORECASE)
#         text = re.sub(r'Mercury\s*in', 'Mercury in', text, flags=re.IGNORECASE)
#         text = re.sub(r'Rahu\s*in', 'Rahu in', text, flags=re.IGNORECASE)
#         text = re.sub(r'Ketu\s*in', 'Ketu in', text, flags=re.IGNORECASE)
        
#         # Fix house references
#         text = re.sub(r'(\d+)(?:st|nd|rd|th)?\s*house', r'\1th house', text, flags=re.IGNORECASE)
#         text = re.sub(r'(\d+)(?:st|nd|rd|th)?\s*bhava', r'\1th bhava', text, flags=re.IGNORECASE)
        
#         # Fix common word breaks
#         text = re.sub(r'indica\s*tes', 'indicates', text, flags=re.IGNORECASE)
#         text = re.sub(r'signi\s*fies', 'signifies', text, flags=re.IGNORECASE)
#         text = re.sub(r'pla\s*cement', 'placement', text, flags=re.IGNORECASE)
        
#         # Remove extra whitespace
#         text = re.sub(r'\s+', ' ', text)
        
#         # Remove page numbers and common PDF artifacts
#         text = re.sub(r'\n\d+\n', '\n', text)  # Remove standalone page numbers
#         text = re.sub(r'\f', '\n', text)  # Replace form feeds with newlines
        
#         # Fix common extraction issues
#         text = text.replace('�', '')  # Remove replacement characters
        
#         # Fix bullet points and dashes
#         text = re.sub(r'•\s*', '. ', text)
#         text = re.sub(r'–\s*', '. ', text)
#         text = re.sub(r'-\s*', '. ', text)
        
#         return text.strip()
    
#     def chunk_into_sentences(self, text: str) -> List[str]:
#         """
#         Split text into sentences for easier processing - enhanced for classical texts
#         """
#         # Split on multiple sentence delimiters
#         sentences = re.split(r'[.!?;]+', text)
        
#         # Clean and filter sentences
#         clean_sentences = []
#         for sentence in sentences:
#             sentence = sentence.strip()
#             # More lenient length requirements for classical texts
#             if 8 <= len(sentence) <= 800:  # Allow longer sentences for classical content
#                 clean_sentences.append(sentence)
        
#         return clean_sentences
    
#     def contains_astrological_content(self, sentence: str) -> bool:
#         """
#         Enhanced check for astrological content including classical patterns
#         """
#         sentence_lower = sentence.lower()
        
#         # Enhanced planet names including Sanskrit/Hindi variants
#         enhanced_planets = self.astro_keywords['planets'] + [
#             'mangal', 'budh', 'brihaspati', 'guru', 'shukra', 'shani', 'surya', 'chandra'
#         ]
        
#         # Enhanced house terms
#         enhanced_houses = self.astro_keywords['houses'] + [
#             'bhava', 'sthana', 'lord', 'lagna', 'ascendant'
#         ]
        
#         # Check for classical rule patterns first
#         classical_patterns = [
#             r'(placement|lord|graha).*?(?:in|of).*?(?:house|bhava)',
#             r'(sun|moon|mars|mercury|jupiter|venus|saturn|rahu|ketu|mangal|budh|shukra|shani|surya|chandra).*?in.*?(?:\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)',
#             r'(?:\d+)(?:st|nd|rd|th)?\s*(?:house|bhava).*?(indicates|signifies|gives|causes)',
#             r'(kuja\s*dosha|rajyoga|yoga|dosha)',
#             r'(indicates|signifies|causes|gives|means).*?(marriage|wealth|health|career|spiritual)'
#         ]
        
#         for pattern in classical_patterns:
#             if re.search(pattern, sentence_lower):
#                 return True
        
#         # Check for planet + house combinations (enhanced)
#         for planet in enhanced_planets:
#             if planet in sentence_lower:
#                 for house_term in enhanced_houses:
#                     if house_term in sentence_lower:
#                         return True
        
#         # Check for planet + sign combinations  
#         for planet in enhanced_planets:
#             if planet in sentence_lower:
#                 for sign in self.astro_keywords['signs']:
#                     if sign in sentence_lower:
#                         return True
        
#         # Check for effect keywords with astrological context
#         effect_keywords = self.astro_keywords['effects'] + [
#             'signifies', 'denotes', 'shows', 'means', 'represents'
#         ]
        
#         for effect in effect_keywords:
#             if effect in sentence_lower:
#                 if any(planet in sentence_lower for planet in enhanced_planets):
#                     return True
#                 if any(house in sentence_lower for house in enhanced_houses):
#                     return True
        
#         # Check for classical terms
#         classical_terms = [
#             'bhava', 'graha', 'yoga', 'dosha', 'karaka', 'lagna', 'arudha',
#             'dasha', 'nakshatra', 'rasi', 'varga', 'sambandha'
#         ]
        
#         if any(term in sentence_lower for term in classical_terms):
#             return True
        
#         return False
    
#     def identify_astrological_content(self, sentences: List[str]) -> List[str]:
#         """
#         Filter sentences to keep only those with astrological content
#         """
#         astrological_sentences = []
        
#         for sentence in sentences:
#             if self.contains_astrological_content(sentence):
#                 astrological_sentences.append(sentence)
        
#         return astrological_sentences
    
#     def process_document(self, pdf_path: str) -> ProcessedDocument:
#         """
#         Complete document processing pipeline
#         """
#         print(f"Processing document: {pdf_path}")
        
#         # Extract text
#         raw_text = self.extract_text(pdf_path)
#         clean_text = self.clean_text(raw_text)
        
#         # Split into sentences
#         sentences = self.chunk_into_sentences(clean_text)
        
#         # Identify astrological content
#         astro_sentences = self.identify_astrological_content(sentences)
        
#         # Get document info
#         filename = Path(pdf_path).name
        
#         print(f"✅ Processed {filename}:")
#         print(f"   Total sentences: {len(sentences)}")
#         print(f"   Astrological sentences: {len(astro_sentences)}")
        
#         return ProcessedDocument(
#             filename=filename,
#             total_pages=0,  # We'll add page counting later
#             extracted_text=clean_text,
#             sentences=sentences,
#             astrological_sentences=astro_sentences
#         )


# # Test/demo functionality
# if __name__ == "__main__":
#     processor = DocumentProcessor()
    
#     # Example usage
#     pdf_path = "data/books/sample_astrology_book.pdf"
    
#     try:
#         result = processor.process_document(pdf_path)
        
#         print(f"\n📊 Processing Results:")
#         print(f"Document: {result.filename}")
#         print(f"Total sentences: {len(result.sentences)}")
#         print(f"Astrological sentences: {len(result.astrological_sentences)}")
        
#         print(f"\n🔍 Sample astrological sentences:")
#         for i, sentence in enumerate(result.astrological_sentences[:5]):
#             print(f"{i+1}. {sentence}")
            
#     except FileNotFoundError:
#         print("❌ Please add a sample PDF to data/books/ to test")
#     except Exception as e:
#         print(f"❌ Error: {e}")