# improved_rule_extractor.py
"""
Enhanced rule extraction system specifically designed for classical astrology texts
Handles OCR issues, complex sentence structures, and improves accuracy
"""

import re
from typing import List, Optional, Dict, Any, Tuple
from .data_models import (
    AstrologicalRule, AstrologicalCondition, AstrologicalEffect, 
    SourceInfo, AuthorityLevel
)


class RuleExtractor:
    """Enhanced rule extractor designed for classical astrology texts with OCR issues"""
    
    def __init__(self):
        # Enhanced planet names including Sanskrit variants
        self.planet_names = {
            'sun': ['sun', 'surya', 'ravi', 'arka', 'aditya', 'soorya'],
            'moon': ['moon', 'chandra', 'soma', 'indu', 'chandrama'],
            'mars': ['mars', 'mangal', 'angaraka', 'bhauma', 'kuja', 'mangala'],
            'mercury': ['mercury', 'budh', 'budha', 'soumya', 'kumar'],
            'jupiter': ['jupiter', 'guru', 'brihaspati', 'devaguru', 'brahmanaspati'],
            'venus': ['venus', 'shukra', 'sukra', 'bhargava', 'ushanas'],
            'saturn': ['saturn', 'shani', 'sanaischara', 'manda', 'shanaischarya'],
            'rahu': ['rahu', 'dragon_head', 'north_node', 'sarpasira'],
            'ketu': ['ketu', 'dragon_tail', 'south_node', 'sikhi']
        }
        
        # Enhanced zodiac signs with additional Sanskrit terms
        self.sign_names = {
            'aries': ['aries', 'mesha', 'ram', 'mesh'],
            'taurus': ['taurus', 'vrishabha', 'bull', 'vrish', 'vrishab'],
            'gemini': ['gemini', 'mithuna', 'twins', 'mithun'],
            'cancer': ['cancer', 'karkata', 'karka', 'crab', 'kark'],
            'leo': ['leo', 'simha', 'lion', 'sinh', 'singh'],
            'virgo': ['virgo', 'kanya', 'virgin', 'kany'],
            'libra': ['libra', 'tula', 'balance', 'tul'],
            'scorpio': ['scorpio', 'vrishchika', 'scorpion', 'vrischik'],
            'sagittarius': ['sagittarius', 'dhanus', 'archer', 'dhan'],
            'capricorn': ['capricorn', 'makara', 'goat', 'makar'],
            'aquarius': ['aquarius', 'kumbha', 'water_bearer', 'kumbh'],
            'pisces': ['pisces', 'meena', 'fish', 'meen']
        }
        
        # House indicators with Sanskrit terms
        self.house_indicators = [
            r'\b(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava|sthana|graha|griha)\b',
            r'\bin\s*the\s*(\d+)(?:st|nd|rd|th)?\b',
            r'\b(\d+)(?:st|nd|rd|th)?\s*from\s*(?:ascendant|lagna)\b'
        ]
        
        # Effect patterns with Sanskrit terms
        self.effect_patterns = {
            'positive': [
                'gives', 'causes', 'brings', 'produces', 'leads to', 'results in',
                'bestows', 'grants', 'blesses with', 'indicates', 'signifies',
                'creates', 'generates', 'manifests', 'yields', 'awards',
                'phala', 'yoga', 'labha', 'prapti', 'karoti'
            ],
            'negative': [
                'destroys', 'damages', 'harms', 'afflicts', 'reduces', 'diminishes',
                'causes loss of', 'takes away', 'removes', 'deprives of',
                'dosha', 'hani', 'nashta', 'kshaya', 'bhanga'
            ]
        }

        # Strength indicators
        self.strength_indicators = {
            'strong': [
                'strong', 'powerful', 'exalted', 'own house', 'own sign',
                'uccha', 'swakshetra', 'swastha', 'digbala', 'balavat'
            ],
            'weak': [
                'weak', 'debilitated', 'combust', 'neecha', 'astangata',
                'durbala', 'mrta', 'khala', 'nipidita'
            ]
        }

        # Aspect patterns with Sanskrit terms
        self.aspect_patterns = [
            r'(?:aspects?|drishti|dristi)\s+(?:to|with|from)?\s+([^,.]+)',
            r'(?:in\s+(?:full|partial)\s+aspect\s+(?:to|with|from)?)\s+([^,.]+)',
            r'(?:receives?\s+(?:full|partial)?\s+aspect\s+(?:from)?)\s+([^,.]+)',
            r'(?:under\s+the\s+aspect\s+of)\s+([^,.]+)'
        ]

        # Astrological condition patterns
        self.condition_patterns = {
            'conjunction': [
                r'(?:conjunction|conjunct|joined|with|along|together|yuti|yukta)\s+(?:with)?\s+([^,.]+)',
                r'(?:in\s+association\s+with)\s+([^,.]+)',
                r'(?:accompanied\s+by)\s+([^,.]+)'
            ],
            'placement': [
                r'(?:placed|situated|posited|located|sthita)\s+(?:in|at)\s+([^,.]+)',
                r'(?:occupies|occupying|residing|residing\s+in)\s+([^,.]+)',
                r'(?:when|if|while)\s+([^,.]+)\s+(?:is|being)\s+in\s+([^,.]+)'
            ],
            'lordship': [
                r'(?:lord|ruler|swami|adhipati)\s+of\s+(?:the)?\s*(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)?',
                r'(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)?\s+(?:lord|ruler|swami|adhipati)',
                r'([^,.]+)\s+being\s+(?:the)?\s+lord\s+of\s+([^,.]+)'
            ],
            'dignity': [
                r'(?:exalted|uccha|in\s+exaltation)\s+(?:in)?\s*([^,.]+)?',
                r'(?:debilitated|neecha|in\s+fall)\s+(?:in)?\s*([^,.]+)?',
                r'(?:own|moolatrikona|swakshetra)\s+(?:sign|house|rashi)\s*([^,.]+)?'
            ],
            'special_yoga': [
                r'(?:forms?|creates?|makes?)\s+(?:a)?\s+([^,.]+)\s+(?:yoga|combination)',
                r'(?:yoga|combination)\s+(?:of|between)\s+([^,.]+)',
                r'(?:in|under\s+the\s+influence\s+of)\s+([^,.]+)\s+(?:yoga|combination)'
            ]
        }
        
        # OCR fixes dictionary
        self.ocr_fixes = {
            'ofthe': 'of the',
            'inthe': 'in the',
            'forthe': 'for the',
            'withthe': 'with the',
            'andthe': 'and the',
            'tothe': 'to the',
            'fromthe': 'from the',
            'bythe': 'by the',
            'onthe': 'on the',
            'asthe': 'as the',
            'isthe': 'is the',
            'atthe': 'at the',
            'thatthe': 'that the',
            'whenthe': 'when the',
            'ifthe': 'if the'
        }
        
        # Enhanced zodiac signs
        self.sign_names = {
            'aries': ['aries', 'mesha', 'ram'],
            'taurus': ['taurus', 'vrishabha', 'bull'],
            'gemini': ['gemini', 'mithuna', 'twins'],
            'cancer': ['cancer', 'karkata', 'karka', 'crab'],
            'leo': ['leo', 'simha', 'lion'],
            'virgo': ['virgo', 'kanya', 'virgin'],
            'libra': ['libra', 'tula', 'balance'],
            'scorpio': ['scorpio', 'vrishchika', 'scorpion'],
            'sagittarius': ['sagittarius', 'dhanus', 'archer'],
            'capricorn': ['capricorn', 'makara', 'goat'],
            'aquarius': ['aquarius', 'kumbha', 'water_bearer'],
            'pisces': ['pisces', 'meena', 'fish']
        }
        
        # House indicators
        self.house_indicators = [
            r'(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)',
            r'(?:house|bhava)\s*(\d+)',
            r'in\s*the\s*(\d+)(?:st|nd|rd|th)?',
            r'(\d+)h\b'
        ]
        
        # Ascendant/Lagna patterns
        self.ascendant_patterns = [
            r'(aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces)\s*(?:ascendant|lagna|rising)',
            r'(?:ascendant|lagna|rising)\s*(?:in\s*)?(aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces)',
            r'for\s*(aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces)\s*(?:ascendant|lagna)'
        ]
        
        # Effect patterns with Sanskrit terms
        self.effect_patterns = {
            'positive': [
                'gives', 'causes', 'brings', 'produces', 'leads to', 'results in',
                'bestows', 'grants', 'blesses with', 'indicates', 'signifies',
                'creates', 'generates', 'manifests', 'yields', 'awards',
                'phala', 'yoga', 'labha', 'prapti', 'karoti'
            ],
            'negative': [
                'destroys', 'damages', 'harms', 'afflicts', 'reduces', 'diminishes',
                'causes loss of', 'takes away', 'removes', 'deprives of',
                'dosha', 'hani', 'nashta', 'kshaya', 'bhanga'
            ]
        }

        # Strength indicators
        self.strength_indicators = {
            'strong': [
                'strong', 'powerful', 'exalted', 'own house', 'own sign',
                'uccha', 'swakshetra', 'swastha', 'digbala', 'balavat'
            ],
            'weak': [
                'weak', 'debilitated', 'combust', 'neecha', 'astangata',
                'durbala', 'mrta', 'khala', 'nipidita'
            ]
        }

        # Aspect patterns with Sanskrit terms
        self.aspect_patterns = [
            r'(?:aspects?|drishti|dristi)\s+(?:to|with|from)?\s+([^,.]+)',
            r'(?:in\s+(?:full|partial)\s+aspect\s+(?:to|with|from)?)\s+([^,.]+)',
            r'(?:receives?\s+(?:full|partial)?\s+aspect\s+(?:from)?)\s+([^,.]+)',
            r'(?:under\s+the\s+aspect\s+of)\s+([^,.]+)'
        ]

        # Common OCR fixes
        self.ocr_fixes = {
            'thesun': 'the sun',
            'themoon': 'the moon',
            'ascen­dant': 'ascendant',
            'ascen-dant': 'ascendant',
            'native­': 'native ',
            'thenative': 'the native',
            'inthe': 'in the',
            'ofthe': 'of the',
            'willbe': 'will be',
            'andthe': 'and the',
            'forthe': 'for the',
            'onthe': 'on the',
            'tothe': 'to the',
            'fromthe': 'from the',
            'ifthe': 'if the',
            'whilethe': 'while the',
            'whenthe': 'when the',
            'asthe': 'as the',
            'bythe': 'by the',
            'withthe': 'with the',
            'overthe': 'over the',
            'underthe': 'under the',
            'aboutthe': 'about the',
            'throughthe': 'through the',
            'againstthe': 'against the',
            'duringthe': 'during the',
            'beforethe': 'before the',
            'afterthe': 'after the',
            'beyondthe': 'beyond the',
            'withinthe': 'within the',
            'withoutthe': 'without the',
            'besidethe': 'beside the',
            'beneaththe': 'beneath the',
            'abovethe': 'above the',
            'aroundthe': 'around the',
            'acrossthe': 'across the',
            'alongthe': 'along the',
            'amongthe': 'among the',
            'betweenthe': 'between the',
            'iff': 'if',
            'aand': 'and',
            'oor': 'or',
            'aan': 'an',
            'sthe': 's the',
            'dthe': 'd the',
            'gthe': 'g the',
            'rthe': 'r the',
            'tthe': 't the',
            'nthe': 'n the',
            'lthe': 'l the',
            'mthe': 'm the',
            'pthe': 'p the',
            'bthe': 'b the',
            'cthe': 'c the',
            'fthe': 'f the',
            'hthe': 'h the',
            'kthe': 'k the',
            'vthe': 'v the',
            'wthe': 'w the',
            'xthe': 'x the',
            'ythe': 'y the',
            'zthe': 'z the'
        }
    
    def clean_ocr_text(self, text):
        # Basic OCR fixes
        for ocr_error, correction in self.ocr_fixes.items():
            text = text.replace(ocr_error, correction)

        # Fix camelCase words
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

        # Handle planet names
        for planet_group in self.planet_names.values():
            for planet in planet_group:
                # Fix planet references
                pattern = f'({planet})(?=[a-z])'
                text = re.sub(pattern, r'\1 ', text, flags=re.IGNORECASE)

        # Handle sign names
        for sign_group in self.sign_names.values():
            for sign in sign_group:
                # Fix sign references
                pattern = f'({sign})(?=[a-z])'
                text = re.sub(pattern, r'\1 ', text, flags=re.IGNORECASE)

        # Fix effect patterns
        for effect_type in self.effect_patterns.values():
            for effect in effect_type:
                pattern = f'({effect})(?=[A-Z][a-z]|[0-9])'
                text = re.sub(pattern, r'\1 ', text, flags=re.IGNORECASE)

        # Fix strength indicators
        for strength_type in self.strength_indicators.values():
            for indicator in strength_type:
                pattern = f'({indicator})(?=[A-Z][a-z]|[0-9])'
                text = re.sub(pattern, r'\1 ', text, flags=re.IGNORECASE)

        # Fix aspect patterns
        for aspect_pattern in self.aspect_patterns:
            text = re.sub(f'({aspect_pattern})(?=[A-Z][a-z]|[0-9])', r'\1 ', text, flags=re.IGNORECASE)

        # Fix condition patterns
        for condition_type in self.condition_patterns.values():
            for pattern in condition_type:
                text = re.sub(f'({pattern})(?=[A-Z][a-z]|[0-9])', r'\1 ', text, flags=re.IGNORECASE)

        # Fix house references
        for house_pattern in self.house_indicators:
            text = re.sub(house_pattern, r' \1 house ', text, flags=re.IGNORECASE)

        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text
    
    def extract_planet_advanced(self, text: str) -> Optional[str]:
        """Advanced planet extraction with variants"""
        text_clean = self.clean_ocr_text(text)
        
        for planet_key, variants in self.planet_names.items():
            for variant in variants:
                if re.search(rf'\b{variant}\b', text_clean):
                    return planet_key.title()
        
        return None
    
    def extract_house_advanced(self, text: str) -> Optional[int]:
        """Advanced house extraction"""
        text_clean = self.clean_ocr_text(text)
        
        # Check for explicit house numbers
        for pattern in self.house_indicators:
            matches = re.findall(pattern, text_clean)
            if matches:
                try:
                    house_num = int(matches[0])
                    if 1 <= house_num <= 12:
                        return house_num
                except (ValueError, IndexError):
                    continue
        
        # Check for lagna/ascendant (1st house)
        if re.search(r'\b(?:lagna|ascendant)\b', text_clean):
            return 1
        
        return None
    
    def extract_sign(self, text: str) -> Optional[str]:
        """Extract zodiac sign from text"""
        text_clean = self.clean_ocr_text(text)
        
        # Check for each sign and its variants
        for sign_key, variants in self.sign_names.items():
            for variant in variants:
                pattern = rf'\b{variant}\b'
                if re.search(pattern, text_clean, re.IGNORECASE):
                    return sign_key.title()
        
        # Check for special patterns
        sign_patterns = [
            r'in\s+(?:the\s+)?sign\s+of\s+([A-Za-z]+)',
            r'placed\s+in\s+([A-Za-z]+)',
            r'posited\s+in\s+([A-Za-z]+)',
            r'occupies\s+([A-Za-z]+)'
        ]
        
        for pattern in sign_patterns:
            match = re.search(pattern, text_clean, re.IGNORECASE)
            if match:
                sign_text = match.group(1).lower()
                for sign_key, variants in self.sign_names.items():
                    if sign_text in variants:
                        return sign_key.title()
        
        return None
    
    def extract_ascendant_context(self, text: str) -> Optional[str]:
        """Extract ascendant context from sentence"""
        text_clean = self.clean_ocr_text(text)
        
        for pattern in self.ascendant_patterns:
            match = re.search(pattern, text_clean)
            if match:
                sign = match.group(1)
                # Normalize sign name
                for sign_key, variants in self.sign_names.items():
                    if sign in variants:
                        return sign_key.title()
        
        return None
    
    def extract_effects_advanced(self, text: str) -> List[AstrologicalEffect]:
        """Enhanced effect extraction"""
        effects = []
        text_clean = self.clean_ocr_text(text)
        
        # Find all effect patterns
        all_indicators = []
        for strength, indicators in self.effect_patterns.items():
            all_indicators.extend([(ind, strength) for ind in indicators])
        
        for indicator, strength in all_indicators:
            pattern = rf'\b{indicator}\b\s*([^.!?]*?)(?:[.!?]|$)'
            matches = re.findall(pattern, text_clean)
            
            for match in matches:
                effect_text = match.strip()
                if len(effect_text) > 5:  # Minimum meaningful length
                    
                    # Determine if positive or negative
                    positive_words = ['wealth', 'prosperity', 'success', 'happiness', 'fortune', 'good', 'beneficial', 'excellent', 'favorable', 'auspicious']
                    negative_words = ['problems', 'difficulties', 'trouble', 'disease', 'death', 'enemy', 'conflict', 'loss', 'bad', 'harmful', 'unfavorable']
                    
                    is_positive = any(word in effect_text for word in positive_words)
                    is_negative = any(word in effect_text for word in negative_words)
                    
                    # Default to positive if unclear
                    positive = is_positive or not is_negative
                    
                    effect = AstrologicalEffect(
                        category=self.categorize_effect_advanced(effect_text),
                        description=effect_text[:150],  # Longer descriptions
                        positive=positive,
                        strength=strength
                    )
                    effects.append(effect)
        
        return effects if effects else [self.create_default_effect()]
    
    def extract_house_number(self, text: str) -> Optional[int]:
        """Extract house number from text"""
        text_clean = self.clean_ocr_text(text)
        
        for pattern in self.house_indicators:
            match = re.search(pattern, text_clean, re.IGNORECASE)
            if match:
                try:
                    house_num = int(match.group(1))
                    if 1 <= house_num <= 12:  # Valid house numbers are 1-12
                        return house_num
                except (ValueError, IndexError):
                    continue
        
        # Try to find direct number references
        number_words = {
            'first': 1, 'second': 2, 'third': 3, 'fourth': 4,
            'fifth': 5, 'sixth': 6, 'seventh': 7, 'eighth': 8,
            'ninth': 9, 'tenth': 10, 'eleventh': 11, 'twelfth': 12
        }
        
        for word, num in number_words.items():
            if word in text_clean.lower():
                return num
        
        return None
    
    def extract_ascendant_context(self, text: str) -> Optional[str]:
        """Extract ascendant context from sentence"""
        text_clean = self.clean_ocr_text(text)
        
        for pattern in self.ascendant_patterns:
            match = re.search(pattern, text_clean)
            if match:
                sign = match.group(1)
                # Normalize sign name
                for sign_key, variants in self.sign_names.items():
                    if sign in variants:
                        return sign_key.title()
        
        return None
    
    def extract_effects_advanced(self, text: str) -> List[AstrologicalEffect]:
        """Enhanced effect extraction"""
        effects = []
        text_clean = self.clean_ocr_text(text)
        
        # Find all effect patterns
        all_indicators = []
        for strength, indicators in self.effect_patterns.items():
            all_indicators.extend([(ind, strength) for ind in indicators])
        
        for indicator, strength in all_indicators:
            pattern = rf'\b{indicator}\b\s*([^.!?]*?)(?:[.!?]|$)'
            matches = re.findall(pattern, text_clean)
            
            for match in matches:
                effect_text = match.strip()
                if len(effect_text) > 5:  # Minimum meaningful length
                    
                    # Determine if positive or negative
                    positive_words = ['wealth', 'prosperity', 'success', 'happiness', 'fortune', 'good', 'beneficial', 'excellent', 'favorable', 'auspicious']
                    negative_words = ['problems', 'difficulties', 'trouble', 'disease', 'death', 'enemy', 'conflict', 'loss', 'bad', 'harmful', 'unfavorable']
                    
                    is_positive = any(word in effect_text for word in positive_words)
                    is_negative = any(word in effect_text for word in negative_words)
                    
                    # Default to positive if unclear
                    positive = is_positive or not is_negative
                    
                    effect = AstrologicalEffect(
                        category=self.categorize_effect_advanced(effect_text),
                        description=effect_text[:150],  # Longer descriptions
                        positive=positive,
                        strength=strength
                    )
                    effects.append(effect)
        
        return effects if effects else [self.create_default_effect()]
    
    def categorize_effect_advanced(self, effect_text: str) -> str:
        """Enhanced effect categorization"""
        categories = {
            'wealth': ['wealth', 'money', 'riches', 'prosperity', 'financial', 'earnings', 'income', 'fortune'],
            'health': ['health', 'disease', 'illness', 'medical', 'body', 'physical', 'ailment', 'cure'],
            'marriage': ['marriage', 'spouse', 'partner', 'relationship', 'wife', 'husband', 'matrimony'],
            'career': ['career', 'job', 'profession', 'work', 'business', 'employment', 'occupation', 'service'],
            'education': ['education', 'learning', 'knowledge', 'study', 'wisdom', 'intelligence', 'scholarship'],
            'spiritual': ['spiritual', 'religious', 'devotion', 'meditation', 'divine', 'sacred', 'temple'],
            'family': ['family', 'children', 'parents', 'siblings', 'brother', 'sister', 'father', 'mother'],
            'travel': ['travel', 'journey', 'foreign', 'abroad', 'distant', 'pilgrimage'],
            'government': ['government', 'king', 'ruler', 'authority', 'power', 'official', 'administrative'],
            'enemies': ['enemy', 'enemies', 'opponent', 'rival', 'adversary', 'competition'],
            'property': ['property', 'land', 'house', 'real estate', 'inheritance', 'patrimony']
        }
        
        effect_lower = effect_text.lower()
        
        for category, keywords in categories.items():
            if any(keyword in effect_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def create_default_effect(self) -> AstrologicalEffect:
        """Create a default effect when none found"""
        return AstrologicalEffect(
            category="general",
            description="General astrological influence",
            positive=True,
            strength="medium"
        )
    
    def calculate_confidence_advanced(self, sentence: str, rule_data: Dict) -> float:
        """Enhanced confidence calculation"""
        confidence = 0.3  # Lower base confidence
        
        # Increase for clear planet identification
        if rule_data.get('planet'):
            confidence += 0.2
        
        # Increase for house identification
        if rule_data.get('house'):
            confidence += 0.15
        
        # Increase for sign identification  
        if rule_data.get('sign'):
            confidence += 0.1
        
        # Increase for ascendant context
        if rule_data.get('ascendant_context'):
            confidence += 0.1
        
        # Increase for meaningful effects
        effects = rule_data.get('effects', [])
        if effects and len(effects[0].description) > 10:
            confidence += 0.15
        
        # Penalty for very short or very long sentences
        word_count = len(sentence.split())
        if word_count < 8:
            confidence -= 0.2
        elif word_count > 60:
            confidence -= 0.1
        
        # Penalty for too many OCR-like artifacts
        ocr_artifacts = len(re.findall(r'[a-z]{15,}', sentence))  # Very long merged words
        if ocr_artifacts > 2:
            confidence -= 0.2
        
        # Bonus for classical astrology terms
        classical_terms = ['yoga', 'dosha', 'dasa', 'bhava', 'graha', 'rasi']
        if any(term in sentence.lower() for term in classical_terms):
            confidence += 0.1
        
        return min(1.0, max(0.1, confidence))
    
    def extract_rule_pattern_1(self, text: str) -> Optional[Dict]:
        """Pattern: 'Planet in House/Sign gives/causes Effect'"""
        text_clean = self.clean_ocr_text(text)
        
        # Enhanced pattern matching
        pattern = rf'({"|".join(["|".join(variants) for variants in self.planet_names.values()])})\s+(?:in\s+(?:the\s+)?)?(?:(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)?\s*)?(?:in\s+)?({"|".join(["|".join(variants) for variants in self.sign_names.values()])})?.*?(?:gives?|causes?|brings?|produces?|results?\s+in|leads?\s+to)\s+([^.!?]*)'
        
        match = re.search(pattern, text_clean, re.IGNORECASE)
        if match:
            planet_raw = match.group(1)
            house_raw = match.group(2)
            sign_raw = match.group(3)
            effect_raw = match.group(4)
            
            # Normalize planet
            planet = None
            for planet_key, variants in self.planet_names.items():
                if planet_raw.lower() in variants:
                    planet = planet_key.title()
                    break
            
            # Parse house
            house = None
            if house_raw:
                try:
                    house = int(house_raw)
                    if not (1 <= house <= 12):
                        house = None
                except ValueError:
                    pass
            
            # Normalize sign
            sign = None
            if sign_raw:
                for sign_key, variants in self.sign_names.items():
                    if sign_raw.lower() in variants:
                        sign = sign_key.title()
                        break
            
            return {
                'planet': planet,
                'house': house,
                'sign': sign,
                'effect_text': effect_raw.strip(),
                'pattern': 'basic_placement'
            }
        
        return None
    
    def extract_rule_pattern_2(self, text: str) -> Optional[Dict]:
        """Pattern: 'For [Sign] ascendant, Planet in House/Sign Effect'"""
        text_clean = self.clean_ocr_text(text)
        
        pattern = rf'(?:for\s+)?({"|".join(["|".join(variants) for variants in self.sign_names.values()])})\s*(?:ascendant|lagna|rising).*?({"|".join(["|".join(variants) for variants in self.planet_names.values()])})\s+(?:in\s+(?:the\s+)?)?(?:(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)?\s*)?(?:in\s+)?({"|".join(["|".join(variants) for variants in self.sign_names.values()])})?.*?(?:gives?|causes?|brings?|produces?|results?\s+in|leads?\s+to)\s+([^.!?]*)'
        
        match = re.search(pattern, text_clean, re.IGNORECASE)
        if match:
            ascendant_raw = match.group(1)
            planet_raw = match.group(2)
            house_raw = match.group(3)
            sign_raw = match.group(4)
            effect_raw = match.group(5)
            
            # Process similar to pattern 1
            planet = None
            for planet_key, variants in self.planet_names.items():
                if planet_raw.lower() in variants:
                    planet = planet_key.title()
                    break
            
            house = None
            if house_raw:
                try:
                    house = int(house_raw)
                    if not (1 <= house <= 12):
                        house = None
                except ValueError:
                    pass
            
            sign = None
            if sign_raw:
                for sign_key, variants in self.sign_names.items():
                    if sign_raw.lower() in variants:
                        sign = sign_key.title()
                        break
            
            ascendant = None
            for sign_key, variants in self.sign_names.items():
                if ascendant_raw.lower() in variants:
                    ascendant = sign_key.title()
                    break
            
            return {
                'planet': planet,
                'house': house,
                'sign': sign,
                'ascendant_context': ascendant,
                'effect_text': effect_raw.strip(),
                'pattern': 'ascendant_specific'
            }
        
        return None
    
    def extract_rule_pattern_3(self, text: str) -> Optional[Dict]:
        """Pattern: 'Planet aspects/conjuncts Planet Effect'"""
        text_clean = self.clean_ocr_text(text)
        
        # Pattern for aspects and conjunctions
        pattern = rf'({"|".join(["|".join(variants) for variants in self.planet_names.values()])})\s+(?:aspects?|conjuncts?|conjoins?|in\s+conjunction\s+with)\s+({"|".join(["|".join(variants) for variants in self.planet_names.values()])}).*?(?:gives?|causes?|brings?|produces?|results?\s+in|leads?\s+to)\s+([^.!?]*)'
        
        match = re.search(pattern, text_clean, re.IGNORECASE)
        if match:
            planet1_raw = match.group(1)
            planet2_raw = match.group(2)
            effect_raw = match.group(3)
            
            # Normalize planets
            planet1 = None
            for planet_key, variants in self.planet_names.items():
                if planet1_raw.lower() in variants:
                    planet1 = planet_key.title()
                    break
            
            planet2 = None
            for planet_key, variants in self.planet_names.items():
                if planet2_raw.lower() in variants:
                    planet2 = planet_key.title()
                    break
            
            if planet1 and planet2:
                return {
                    'planet': planet1,
                    'aspect_planet': planet2,
                    'effect_text': effect_raw.strip(),
                    'pattern': 'aspect_conjunction'
                }
        
        return None
    
    def extract_rule_pattern_4(self, text: str) -> Optional[Dict]:
        """Pattern: 'Lord of House in House/Sign Effect'"""
        text_clean = self.clean_ocr_text(text)
        
        # Pattern for house lordship
        pattern = rf'(?:lord|ruler)\s+of\s+(?:the\s+)?(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)?\s+(?:in|placed\s+in|posited\s+in)\s+(?:the\s+)?(?:(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)?|({"|".join(["|".join(variants) for variants in self.sign_names.values()])})).*?(?:gives?|causes?|brings?|produces?|results?\s+in|leads?\s+to)\s+([^.!?]*)'
        
        match = re.search(pattern, text_clean, re.IGNORECASE)
        if match:
            lord_house_raw = match.group(1)
            placed_house_raw = match.group(2)
            placed_sign_raw = match.group(3)
            effect_raw = match.group(4)
            
            # Parse house numbers
            lord_house = None
            placed_house = None
            try:
                if lord_house_raw:
                    lord_house = int(lord_house_raw)
                    if not (1 <= lord_house <= 12):
                        lord_house = None
                
                if placed_house_raw:
                    placed_house = int(placed_house_raw)
                    if not (1 <= placed_house <= 12):
                        placed_house = None
            except ValueError:
                pass
            
            # Parse sign
            placed_sign = None
            if placed_sign_raw:
                for sign_key, variants in self.sign_names.items():
                    if placed_sign_raw.lower() in variants:
                        placed_sign = sign_key.title()
                        break
            
            if lord_house and (placed_house or placed_sign):
                return {
                    'lord_of_house': lord_house,
                    'house': placed_house,
                    'sign': placed_sign,
                    'effect_text': effect_raw.strip(),
                    'pattern': 'house_lordship'
                }
        
        return None
    
    def extract_rule_pattern_5(self, text: str) -> Optional[Dict]:
        """Pattern: 'Planet in Nakshatra Effect'"""
        text_clean = self.clean_ocr_text(text)
        
        # Extended nakshatra list
        nakshatras = [
            'ashwini', 'bharani', 'krittika', 'rohini', 'mrigashira', 'ardra',
            'punarvasu', 'pushya', 'ashlesha', 'magha', 'purva phalguni', 'uttara phalguni',
            'hasta', 'chitra', 'swati', 'vishakha', 'anuradha', 'jyeshtha',
            'mula', 'purva ashadha', 'uttara ashadha', 'shravana', 'dhanishta',
            'shatabhisha', 'purva bhadrapada', 'uttara bhadrapada', 'revati'
        ]
        
        pattern = rf'({"|".join(["|".join(variants) for variants in self.planet_names.values()])})\s+(?:in|placed\s+in)\s+({"|".join(nakshatras)})\s*(?:nakshatra)?.*?(?:gives?|causes?|brings?|produces?|results?\s+in|leads?\s+to)\s+([^.!?]*)'
        
        match = re.search(pattern, text_clean, re.IGNORECASE)
        if match:
            planet_raw = match.group(1)
            nakshatra_raw = match.group(2)
            effect_raw = match.group(3)
            
            # Normalize planet
            planet = None
            for planet_key, variants in self.planet_names.items():
                if planet_raw.lower() in variants:
                    planet = planet_key.title()
                    break
            
            if planet and nakshatra_raw:
                return {
                    'planet': planet,
                    'nakshatra': nakshatra_raw.title(),
                    'effect_text': effect_raw.strip(),
                    'pattern': 'nakshatra_placement'
                }
        
        return None
    
    def extract_rule_pattern_6(self, text: str) -> Optional[Dict]:
        """Pattern: 'Yoga combinations and special configurations'"""
        text_clean = self.clean_ocr_text(text)
        
        # Common yoga patterns
        yoga_patterns = [
            r'(raj\s*yoga|dhana\s*yoga|yoga\s+of.*?|.*?\s+yoga)\s+(?:is\s+formed|forms|gives|causes|brings)\s+([^.!?]*)',
            r'(?:when|if)\s+([^.!?]*?)\s+(?:forms?|creates?|makes?)\s+(?:a\s+)?yoga.*?(?:gives?|causes?|brings?)\s+([^.!?]*)',
            r'(?:combination|configuration)\s+of\s+([^.!?]*?)\s+(?:gives?|causes?|brings?|produces?)\s+([^.!?]*)'
        ]
        
        for pattern in yoga_patterns:
            match = re.search(pattern, text_clean, re.IGNORECASE)
            if match:
                yoga_desc = match.group(1)
                effect_raw = match.group(2)
                
                return {
                    'yoga_type': yoga_desc.strip(),
                    'effect_text': effect_raw.strip(),
                    'pattern': 'yoga_combination'
                }
        
        return None

    def extract_rule_from_sentence_improved(self, sentence: str, source_info: SourceInfo) -> Optional[AstrologicalRule]:
        """Main improved rule extraction method with all patterns"""
        
        # Try different patterns in order of specificity
        rule_data = None
        
        # Pattern 1: Basic placement (Planet in House/Sign gives Effect)
        rule_data = self.extract_rule_pattern_1(sentence)
        
        # Pattern 2: Ascendant specific (For Sign ascendant, Planet in House/Sign Effect)
        if not rule_data:
            rule_data = self.extract_rule_pattern_2(sentence)
        
        # Pattern 3: Aspects and conjunctions
        if not rule_data:
            rule_data = self.extract_rule_pattern_3(sentence)
        
        # Pattern 4: House lordship
        if not rule_data:
            rule_data = self.extract_rule_pattern_4(sentence)
        
        # Pattern 5: Nakshatra placement
        if not rule_data:
            rule_data = self.extract_rule_pattern_5(sentence)
        
        # Pattern 6: Yoga combinations
        if not rule_data:
            rule_data = self.extract_rule_pattern_6(sentence)
        
        # Fallback to basic extraction
        if not rule_data:
            planet = self.extract_planet_advanced(sentence)
            house = self.extract_house_advanced(sentence)
            sign = self.extract_sign(sentence)
            ascendant = self.extract_ascendant_context(sentence)
            
            if planet and (house or sign):
                effects = self.extract_effects_advanced(sentence)
                rule_data = {
                    'planet': planet,
                    'house': house,
                    'sign': sign,
                    'ascendant_context': ascendant,
                    'effects': effects,
                    'pattern': 'fallback'
                }
        
        if not rule_data:
            return None
        
        try:
            # Create conditions based on pattern type
            additional_conditions = {}
            
            if rule_data.get('ascendant_context'):
                additional_conditions['ascendant_context'] = rule_data['ascendant_context']
            if rule_data.get('pattern'):
                additional_conditions['extraction_pattern'] = rule_data['pattern']
            if rule_data.get('aspect_planet'):
                additional_conditions['aspect_planet'] = rule_data['aspect_planet']
            if rule_data.get('lord_of_house'):
                additional_conditions['lord_of_house'] = rule_data['lord_of_house']
            if rule_data.get('yoga_type'):
                additional_conditions['yoga_type'] = rule_data['yoga_type']
            
            conditions = AstrologicalCondition(
                planet=rule_data.get('planet'),
                house=rule_data.get('house'),
                sign=rule_data.get('sign'),
                nakshatra=rule_data.get('nakshatra'),
                additional_conditions=additional_conditions if additional_conditions else None
            )
            
            # Create effects
            if 'effects' in rule_data:
                effects = rule_data['effects']
            elif 'effect_text' in rule_data:
                effects = [AstrologicalEffect(
                    category=self.categorize_effect_advanced(rule_data['effect_text']),
                    description=rule_data['effect_text'][:150],
                    positive=not any(neg in rule_data['effect_text'].lower() for neg in ['problem', 'disease', 'trouble', 'conflict']),
                    strength="medium"
                )]
            else:
                effects = [self.create_default_effect()]
            
            # Generate tags
            tags = []
            if conditions.planet:
                tags.append(f"planet:{conditions.planet.lower()}")
            if conditions.house:
                tags.append(f"house:{conditions.house}")
            if conditions.sign:
                tags.append(f"sign:{conditions.sign.lower()}")
            if conditions.nakshatra:
                tags.append(f"nakshatra:{conditions.nakshatra.lower()}")
            if rule_data.get('ascendant_context'):
                tags.append(f"ascendant:{rule_data['ascendant_context'].lower()}")
            if rule_data.get('pattern'):
                tags.append(f"pattern:{rule_data['pattern']}")
            if rule_data.get('aspect_planet'):
                tags.append(f"aspect:{rule_data['aspect_planet'].lower()}")
            if rule_data.get('yoga_type'):
                tags.append(f"yoga:{rule_data['yoga_type'].lower()}")
            
            for effect in effects:
                tags.append(f"category:{effect.category}")
                if not effect.positive:
                    tags.append("negative")
            
            # Calculate confidence
            confidence = self.calculate_confidence_advanced(sentence, rule_data)
            
            # Create rule
            rule = AstrologicalRule(
                id="",  # Will be auto-generated
                original_text=sentence.strip(),
                conditions=conditions,
                effects=effects,
                source=source_info,
                tags=tags,
                confidence_score=confidence
            )
            
            return rule
            
        except Exception as e:
            print(f"Error creating improved rule: {e}")
            return None
    
    def extract_rules_from_sentences(self, sentences: List[str], source_info: SourceInfo) -> List[AstrologicalRule]:
        """
        Enhanced rule extraction from sentences with multiple strategies for maximum extraction
        Uses progressively relaxed criteria to capture more rules from classical texts
        """
        rules = []
        rule_counter = 1
        
        print(f"🔄 Processing {len(sentences)} astrological sentences for rule extraction...")
        
        for i, sentence in enumerate(sentences):
            if i % 100 == 0:  # Progress indicator
                print(f"   Progress: {i}/{len(sentences)} sentences processed...")
            
            # Strategy 1: Use the improved extraction method (most comprehensive)
            rule = self.extract_rule_from_sentence_improved(sentence, source_info)
            
            if rule:
                rule.id = f"{source_info.title.lower().replace(' ', '_')}_{rule_counter}"
                rules.append(rule)
                rule_counter += 1
                continue
            
            # Strategy 2: Fallback with relaxed requirements - just need astrological content
            cleaned_text = self.clean_ocr_text(sentence)
            
            # Try to extract any astrological components
            planet = self.extract_planet_advanced(cleaned_text)
            house = self.extract_house_advanced(cleaned_text)
            sign = self.extract_sign(cleaned_text)
            ascendant = self.extract_ascendant_context(cleaned_text)
            
            # Create rule if we have ANY meaningful astrological component
            should_create_rule = False
            confidence_base = 0.2  # Lower base confidence for relaxed extraction
            
            # Primary criteria: Planet with any context
            if planet and (house or sign or ascendant):
                should_create_rule = True
                confidence_base = 0.4
            
            # Secondary criteria: House with any context  
            elif house and (sign or ascendant):
                should_create_rule = True
                confidence_base = 0.3
            
            # Tertiary criteria: Multiple components without planet
            elif house and sign:
                should_create_rule = True
                confidence_base = 0.25
            
            # Quaternary criteria: Strong astrological keywords
            elif any(keyword in cleaned_text.lower() for keyword in [
                'yoga', 'dosha', 'dasa', 'bhava', 'graha', 'rasi', 'nakshatra',
                'exalted', 'debilitated', 'moolatrikona', 'aspects', 'conjunction',
                'lord of', 'ruler of', 'placed in', 'posited in', 'occupies'
            ]):
                should_create_rule = True
                confidence_base = 0.2
            
            if should_create_rule:
                try:
                    # Extract effects with relaxed criteria
                    effects = self.extract_effects_advanced(cleaned_text)
                    if not effects:
                        # Create a general effect if none found
                        effects = [AstrologicalEffect(
                            category=self.categorize_effect_from_sentence(cleaned_text),
                            description=self.extract_general_effect(cleaned_text),
                            positive=self.determine_effect_polarity(cleaned_text),
                            strength="medium"
                        )]
                    
                    # Create condition
                    condition = AstrologicalCondition(
                        planet=planet,
                        house=house,
                        sign=sign,
                        additional_conditions={
                            'ascendant_context': ascendant,
                            'extraction_method': 'relaxed_fallback',
                            'raw_sentence': cleaned_text[:100]  # Keep part of original for context
                        } if ascendant else {'extraction_method': 'relaxed_fallback'}
                    )
                    
                    # Calculate confidence with additional factors
                    confidence = self.calculate_relaxed_confidence(cleaned_text, {
                        'planet': planet,
                        'house': house, 
                        'sign': sign,
                        'ascendant': ascendant,
                        'effects': effects
                    })
                    
                    # Generate comprehensive tags
                    tags = []
                    if planet:
                        tags.append(f"planet:{planet.lower()}")
                    if house:
                        tags.append(f"house:{house}")
                    if sign:
                        tags.append(f"sign:{sign.lower()}")
                    if ascendant:
                        tags.append(f"ascendant:{ascendant.lower()}")
                    
                    # Add effect-based tags
                    for effect in effects:
                        tags.append(f"category:{effect.category}")
                        if not effect.positive:
                            tags.append("negative")
                    
                    # Add extraction method tag
                    tags.append("method:relaxed")
                    
                    # Create rule
                    rule = AstrologicalRule(
                        id=f"{source_info.title.lower().replace(' ', '_')}_{rule_counter}",
                        original_text=sentence.strip(),
                        conditions=condition,
                        effects=effects,
                        source=source_info,
                        tags=tags,
                        confidence_score=confidence
                    )
                    
                    rules.append(rule)
                    rule_counter += 1
                    
                except Exception as e:
                    print(f"Warning: Error creating relaxed rule from '{sentence[:50]}...': {e}")
                    continue
        
        print(f"✅ Extraction complete: {len(rules)} rules extracted from {len(sentences)} sentences")
        return rules
    
    def calculate_relaxed_confidence(self, sentence: str, components: Dict) -> float:
        """Calculate confidence for relaxed extraction with lower thresholds"""
        confidence = 0.15  # Lower base confidence
        
        # Component-based scoring
        if components.get('planet'):
            confidence += 0.2
        if components.get('house'):
            confidence += 0.15
        if components.get('sign'):
            confidence += 0.1
        if components.get('ascendant'):
            confidence += 0.1
        
        # Effect quality scoring
        effects = components.get('effects', [])
        if effects and effects[0].description and len(effects[0].description) > 5:
            confidence += 0.1
        
        # Sentence quality factors
        word_count = len(sentence.split())
        
        # Optimal length bonus
        if 10 <= word_count <= 50:
            confidence += 0.1
        elif 8 <= word_count <= 60:
            confidence += 0.05
        
        # Classical terms bonus
        classical_bonus_terms = [
            'yoga', 'dosha', 'dasa', 'bhava', 'graha', 'rasi', 'nakshatra',
            'uccha', 'neecha', 'swakshetra', 'moolatrikona', 'digbala',
            'lord', 'ruler', 'aspect', 'conjunction', 'trine', 'square'
        ]
        
        classical_count = sum(1 for term in classical_bonus_terms if term in sentence.lower())
        confidence += min(0.15, classical_count * 0.03)
        
        # Astrological structure bonus
        structure_patterns = [
            r'if\s+.*?\s+then\s+.*',  # Conditional structure
            r'when\s+.*?\s+.*',       # Temporal structure  
            r'.*?\s+gives?\s+.*',     # Causal structure
            r'.*?\s+causes?\s+.*',    # Causal structure
            r'.*?\s+results?\s+in\s+.*'  # Result structure
        ]
        
        for pattern in structure_patterns:
            if re.search(pattern, sentence.lower()):
                confidence += 0.05
                break
        
        # Penalty for very poor quality indicators
        if len(re.findall(r'[a-z]{20,}', sentence)) > 1:  # Too many merged words
            confidence -= 0.1
        
        if sentence.count('?') > 2 or sentence.count('!') > 2:  # Too much punctuation
            confidence -= 0.05
        
        return min(0.95, max(0.1, confidence))  # Clamp between 0.1 and 0.95
    
    def categorize_effect_from_sentence(self, sentence: str) -> str:
        """Categorize effect based on sentence content when no explicit effect found"""
        sentence_lower = sentence.lower()
        
        # Enhanced categorization keywords
        category_keywords = {
            'wealth': ['wealth', 'money', 'riches', 'prosperity', 'financial', 'dhan', 'sampatti'],
            'health': ['health', 'disease', 'illness', 'body', 'medical', 'roga', 'arogya'],
            'marriage': ['marriage', 'spouse', 'partner', 'wife', 'husband', 'vivah', 'patni'],
            'career': ['career', 'job', 'profession', 'work', 'business', 'karma', 'vyavasaya'],
            'education': ['education', 'learning', 'knowledge', 'study', 'vidya', 'gyan'],
            'family': ['children', 'parents', 'siblings', 'family', 'putra', 'mata', 'pita'],
            'spiritual': ['spiritual', 'religious', 'devotion', 'dharma', 'moksha', 'tapas'],
            'government': ['king', 'ruler', 'authority', 'government', 'raja', 'adhikari'],
            'travel': ['travel', 'journey', 'foreign', 'pravasa', 'yatra'],
            'enemies': ['enemy', 'enemies', 'opponent', 'satru', 'ari'],
            'property': ['property', 'land', 'house', 'bhumi', 'griha'],
            'fortune': ['fortune', 'luck', 'destiny', 'bhagya', 'daiva']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in sentence_lower for keyword in keywords):
                return category
        
        # Fallback based on house context
        house_categories = {
            1: 'personality', 2: 'wealth', 3: 'siblings', 4: 'family', 
            5: 'children', 6: 'enemies', 7: 'marriage', 8: 'longevity',
            9: 'fortune', 10: 'career', 11: 'gains', 12: 'losses'
        }
        
        for house_num, category in house_categories.items():
            if f'{house_num}' in sentence_lower and 'house' in sentence_lower:
                return category
        
        return 'general'
    
    def extract_general_effect(self, sentence: str) -> str:
        """Extract a general effect description when specific effects not found"""
        # Try to find any outcome or result description
        effect_indicators = [
            r'(?:gives?|causes?|brings?|produces?|results?\s+in|leads?\s+to)\s+([^.!?]*)',
            r'(?:will\s+have|will\s+get|will\s+be|will\s+become)\s+([^.!?]*)',
            r'(?:makes?|renders?|creates?)\s+([^.!?]*)',
            r'(?:indicates?|signifies?|shows?)\s+([^.!?]*)'
        ]
        
        for pattern in effect_indicators:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                effect_text = match.group(1).strip()
                if len(effect_text) > 3:
                    return effect_text[:100]  # Limit length
        
        # If no explicit effect found, create contextual effect
        if any(term in sentence.lower() for term in ['good', 'beneficial', 'auspicious', 'favorable']):
            return "beneficial astrological influence"
        elif any(term in sentence.lower() for term in ['bad', 'harmful', 'inauspicious', 'unfavorable']):
            return "challenging astrological influence"
        else:
            return "notable astrological influence"
    
    def determine_effect_polarity(self, sentence: str) -> bool:
        """Determine if effect is positive or negative based on sentence content"""
        sentence_lower = sentence.lower()
        
        positive_indicators = [
            'good', 'beneficial', 'auspicious', 'favorable', 'excellent', 'great',
            'prosperity', 'success', 'happiness', 'wealth', 'fortune', 'blessed',
            'shubha', 'mangal', 'uttam', 'accha'
        ]
        
        negative_indicators = [
            'bad', 'harmful', 'inauspicious', 'unfavorable', 'difficult', 'trouble',
            'disease', 'loss', 'enemy', 'conflict', 'problem', 'suffering',
            'ashubha', 'papa', 'dukha', 'roga', 'klesh'
        ]
        
        positive_score = sum(1 for word in positive_indicators if word in sentence_lower)
        negative_score = sum(1 for word in negative_indicators if word in sentence_lower)
        
        # Default to positive if unclear
        return positive_score >= negative_score


# Test function
def test_improved_extractor():
    """Test the improved extractor with sample data"""
    
    extractor = ImprovedRuleExtractor()
    source = SourceInfo(title="Test", authority_level=AuthorityLevel.CLASSICAL)
    
    test_sentences = [
        "JatakaJambunadeeyam addsthattheSuninAriesindentical withascendant gives wealth",
        "ForTaurus Lagna,theSunin4thinLeo,willgivegood employmental careerwhileinthe3rdforGemini ascen­ dant,itgivesonlyonebrother whowillbeveryfamous",
        "Cancerascendant: The Mooninthe12thiffullwillkeepthenativefreefrom diseases andifwaningcausesdiseases fromchikihood till theend"
    ]
    
    print("🧪 Testing Improved Rule Extractor")
    print("=" * 50)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n{i}. Input: {sentence}")
        print(f"   Cleaned: {extractor.clean_ocr_text(sentence)}")
        
        rule = extractor.extract_rule_from_sentence_improved(sentence, source)
        
        if rule:
            print(f"   ✅ Planet: {rule.conditions.planet}")
            print(f"   ✅ House: {rule.conditions.house}")
            print(f"   ✅ Sign: {rule.conditions.sign}")
            print(f"   ✅ Effects: {[e.description[:50] + '...' for e in rule.effects]}")
            print(f"   ✅ Confidence: {rule.confidence_score:.2f}")
            print(f"   ✅ Tags: {rule.tags}")
        else:
            print("   ❌ No rule extracted")


if __name__ == "__main__":
    test_improved_extractor()