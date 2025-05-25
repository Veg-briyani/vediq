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
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page numbers and common PDF artifacts
        text = re.sub(r'\n\d+\n', '\n', text)
        text = re.sub(r'\f', '\n', text)
        # Fix common extraction issues
        text = text.replace('�', '')
        return text.strip()
    
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