# src/rule_extractor.py
"""
Rule extraction system for converting astrological text into structured rules
"""

import re
from typing import List, Optional, Dict, Any, Tuple
from data_models import (
    AstrologicalRule, AstrologicalCondition, AstrologicalEffect, 
    SourceInfo, AuthorityLevel, create_simple_rule
)


class RuleExtractor:
    """
    Extracts structured astrological rules from natural language text
    """
    
    def __init__(self):
        # Define patterns for parsing astrological statements
        self.planet_names = [
            'sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 
            'rahu', 'ketu', 'lagna', 'ascendant'
        ]
        
        self.sign_names = [
            'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
            'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
        ]
        
        self.house_patterns = [
            r'(\d+)(?:st|nd|rd|th)?\s+house',
            r'house\s+(\d+)',
            r'(\d+)h',
            r'lagna|ascendant'  # 1st house equivalents
        ]
        
        self.effect_indicators = [
            'gives', 'brings', 'causes', 'results in', 'leads to', 'produces',
            'indicates', 'shows', 'denotes', 'signifies', 'makes', 'creates'
        ]
        
        self.positive_effects = [
            'wealth', 'prosperity', 'success', 'happiness', 'wisdom', 'fortune',
            'good', 'beneficial', 'auspicious', 'favorable', 'excellent'
        ]
        
        self.negative_effects = [
            'problems', 'difficulties', 'obstacles', 'conflicts', 'trouble',
            'bad', 'harmful', 'inauspicious', 'unfavorable', 'loss'
        ]
    
    def extract_planet(self, text: str) -> Optional[str]:
        """Extract planet name from text"""
        text_lower = text.lower()
        
        for planet in self.planet_names:
            if planet in text_lower:
                return planet.title()
        
        return None
    
    def extract_house(self, text: str) -> Optional[int]:
        """Extract house number from text"""
        text_lower = text.lower()
        
        # Handle special cases first
        if 'lagna' in text_lower or 'ascendant' in text_lower:
            return 1
        
        # Try each house pattern
        for pattern in self.house_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    house_num = int(matches[0])
                    if 1 <= house_num <= 12:
                        return house_num
                except ValueError:
                    continue
        
        return None
    
    def extract_sign(self, text: str) -> Optional[str]:
        """Extract zodiac sign from text"""
        text_lower = text.lower()
        
        for sign in self.sign_names:
            if sign in text_lower:
                return sign.title()
        
        return None
    
    def extract_effects(self, text: str) -> List[AstrologicalEffect]:
        """Extract effects from text"""
        effects = []
        text_lower = text.lower()
        
        # Split text around effect indicators
        for indicator in self.effect_indicators:
            if indicator in text_lower:
                # Get text after the indicator
                parts = text_lower.split(indicator, 1)
                if len(parts) > 1:
                    effect_text = parts[1].strip()
                    
                    # Determine if effect is positive or negative
                    is_positive = any(pos in effect_text for pos in self.positive_effects)
                    is_negative = any(neg in effect_text for neg in self.negative_effects)
                    
                    # Default to positive if unclear
                    positive = is_positive or not is_negative
                    
                    # Extract category
                    category = self.categorize_effect(effect_text)
                    
                    effect = AstrologicalEffect(
                        category=category,
                        description=effect_text[:100],  # Limit description length
                        positive=positive,
                        strength="medium"
                    )
                    effects.append(effect)
        
        # If no effects found, create a general one
        if not effects:
            effect = AstrologicalEffect(
                category="general",
                description="General astrological effect",
                positive=True
            )
            effects.append(effect)
        
        return effects
    
    def categorize_effect(self, effect_text: str) -> str:
        """Categorize the type of effect"""
        categories = {
            'wealth': ['money', 'wealth', 'riches', 'prosperity', 'financial'],
            'health': ['health', 'disease', 'illness', 'medical', 'body'],
            'marriage': ['marriage', 'spouse', 'partner', 'relationship'],
            'career': ['career', 'job', 'profession', 'work', 'business'],
            'education': ['education', 'learning', 'knowledge', 'study'],
            'spiritual': ['spiritual', 'religious', 'devotion', 'meditation'],
            'family': ['family', 'children', 'parents', 'siblings'],
            'travel': ['travel', 'journey', 'foreign', 'abroad']
        }
        
        effect_lower = effect_text.lower()
        
        for category, keywords in categories.items():
            if any(keyword in effect_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def extract_conditions(self, text: str) -> AstrologicalCondition:
        """Extract all conditions from text"""
        planet = self.extract_planet(text)
        house = self.extract_house(text)
        sign = self.extract_sign(text)
        
        # Look for additional conditions
        additional = {}
        text_lower = text.lower()
        
        # Check for exaltation/debilitation
        if 'exalted' in text_lower or 'exaltation' in text_lower:
            additional['exalted'] = True
        elif 'debilitated' in text_lower or 'debilitation' in text_lower:
            additional['debilitated'] = True
        
        # Check for own sign
        if 'own sign' in text_lower or 'own house' in text_lower:
            additional['own_sign'] = True
        
        # Check for aspects
        if 'aspect' in text_lower:
            additional['has_aspect'] = True
        
        return AstrologicalCondition(
            planet=planet,
            house=house,
            sign=sign,
            additional_conditions=additional if additional else None
        )
    
    def is_valid_rule_sentence(self, sentence: str) -> bool:
        """Check if a sentence contains a valid astrological rule"""
        # Must have a planet
        if not self.extract_planet(sentence):
            return False
        
        # Must have either house or sign
        house = self.extract_house(sentence)
        sign = self.extract_sign(sentence)
        
        if not house and not sign:
            return False
        
        # Must have an effect indicator
        text_lower = sentence.lower()
        has_effect = any(indicator in text_lower for indicator in self.effect_indicators)
        
        return has_effect
    
    def extract_rule_from_sentence(self, sentence: str, source_info: SourceInfo) -> Optional[AstrologicalRule]:
        """Extract a complete rule from a single sentence"""
        
        if not self.is_valid_rule_sentence(sentence):
            return None
        
        try:
            conditions = self.extract_conditions(sentence)
            effects = self.extract_effects(sentence)
            
            # Generate tags based on content
            tags = []
            if conditions.planet:
                tags.append(f"planet:{conditions.planet.lower()}")
            if conditions.house:
                tags.append(f"house:{conditions.house}")
            if conditions.sign:
                tags.append(f"sign:{conditions.sign.lower()}")
            
            for effect in effects:
                tags.append(f"category:{effect.category}")
                if not effect.positive:
                    tags.append("negative")
            
            rule = AstrologicalRule(
                id="",  # Will be auto-generated
                original_text=sentence.strip(),
                conditions=conditions,
                effects=effects,
                source=source_info,
                tags=tags,
                confidence_score=self.calculate_confidence(sentence, conditions, effects)
            )
            
            return rule
            
        except Exception as e:
            print(f"Error extracting rule from sentence: {e}")
            return None
    
    def calculate_confidence(self, sentence: str, conditions: AstrologicalCondition, 
                           effects: List[AstrologicalEffect]) -> float:
        """Calculate confidence score for extracted rule"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence for specific conditions
        if conditions.planet:
            confidence += 0.2
        if conditions.house:
            confidence += 0.15
        if conditions.sign:
            confidence += 0.1
        
        # Increase confidence for clear effects
        if len(effects) > 0 and effects[0].description:
            confidence += 0.1
        
        # Decrease confidence for very short or very long sentences
        sentence_length = len(sentence.split())
        if sentence_length < 5 or sentence_length > 50:
            confidence -= 0.1
        
        return min(1.0, max(0.1, confidence))
    
    def extract_rules_from_sentences(self, sentences: List[str], 
                                   source_info: SourceInfo) -> List[AstrologicalRule]:
        """Extract rules from a list of sentences"""
        
        rules = []
        
        for sentence in sentences:
            rule = self.extract_rule_from_sentence(sentence, source_info)
            if rule:
                rules.append(rule)
        
        return rules
    
    def extract_rules_batch(self, sentence_groups: List[Tuple[List[str], SourceInfo]]) -> List[AstrologicalRule]:
        """Extract rules from multiple documents/sources"""
        
        all_rules = []
        
        for sentences, source_info in sentence_groups:
            rules = self.extract_rules_from_sentences(sentences, source_info)
            all_rules.extend(rules)
            
            print(f"Extracted {len(rules)} rules from {source_info.title}")
        
        return all_rules


# Utility functions for testing and debugging

def demo_rule_extraction():
    """Demo function to test rule extraction"""
    
    extractor = RuleExtractor()
    
    # Test sentences
    test_sentences = [
        "Mars in the 7th house causes conflicts in marriage",
        "Jupiter in its own sign gives wisdom and prosperity",
        "Sun in the 10th house brings success in career",
        "Moon in Cancer indicates emotional nature",
        "Saturn in the 12th house leads to spiritual growth but causes delays",
        "Venus exalted in Pisces gives artistic talents"
    ]
    
    source = SourceInfo(
        title="Test Astrology Book",
        author="Test Author",
        authority_level=AuthorityLevel.TRADITIONAL
    )
    
    print("🧪 Testing Rule Extraction")
    print("=" * 40)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n{i}. Input: {sentence}")
        
        rule = extractor.extract_rule_from_sentence(sentence, source)
        
        if rule:
            print(f"   ✅ Planet: {rule.conditions.planet}")
            print(f"   ✅ House: {rule.conditions.house}")
            print(f"   ✅ Sign: {rule.conditions.sign}")
            print(f"   ✅ Effects: {len(rule.effects)}")
            print(f"   ✅ Confidence: {rule.confidence_score:.2f}")
            print(f"   ✅ Tags: {', '.join(rule.tags)}")
        else:
            print("   ❌ No rule extracted")


if __name__ == "__main__":
    demo_rule_extraction()






# This code is part of the Astrology AI project.
# It is designed to extract structured astrological rules from natural language text.
# The project is open-source and available on GitHub.
# src/rule_extractor.py
# """
# Rule extraction system for converting astrological text into structured rules
# """

# import re
# from typing import List, Optional, Dict, Any, Tuple
# from data_models import (
#     AstrologicalRule, AstrologicalCondition, AstrologicalEffect, 
#     SourceInfo, AuthorityLevel, create_simple_rule
# )


# class RuleExtractor:
#     """
#     Extracts structured astrological rules from natural language text
#     """
    
#     def __init__(self):
#         # Define patterns for parsing astrological statements
#         self.planet_names = [
#             'sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 
#             'rahu', 'ketu', 'lagna', 'ascendant'
#         ]
        
#         self.sign_names = [
#             'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
#             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
#         ]
        
#         self.house_patterns = [
#             r'(\d+)(?:st|nd|rd|th)?\s+house',
#             r'house\s+(\d+)',
#             r'(\d+)h',
#             r'lagna|ascendant'  # 1st house equivalents
#         ]
        
#         self.effect_indicators = [
#             'gives', 'brings', 'causes', 'results in', 'leads to', 'produces',
#             'indicates', 'shows', 'denotes', 'signifies', 'makes', 'creates'
#         ]
        
#         self.positive_effects = [
#             'wealth', 'prosperity', 'success', 'happiness', 'wisdom', 'fortune',
#             'good', 'beneficial', 'auspicious', 'favorable', 'excellent'
#         ]
        
#         self.negative_effects = [
#             'problems', 'difficulties', 'obstacles', 'conflicts', 'trouble',
#             'bad', 'harmful', 'inauspicious', 'unfavorable', 'loss'
#         ]
    
#     def extract_planet(self, text: str) -> Optional[str]:
#         """Extract planet name from text"""
#         text_lower = text.lower()
        
#         for planet in self.planet_names:
#             if planet in text_lower:
#                 return planet.title()
        
#         return None
    
#     def extract_house(self, text: str) -> Optional[int]:
#         """Extract house number from text"""
#         text_lower = text.lower()
        
#         # Handle special cases first
#         if 'lagna' in text_lower or 'ascendant' in text_lower:
#             return 1
        
#         # Try each house pattern
#         for pattern in self.house_patterns:
#             matches = re.findall(pattern, text_lower)
#             if matches:
#                 try:
#                     house_num = int(matches[0])
#                     if 1 <= house_num <= 12:
#                         return house_num
#                 except ValueError:
#                     continue
        
#         return None
    
#     def extract_sign(self, text: str) -> Optional[str]:
#         """Extract zodiac sign from text"""
#         text_lower = text.lower()
        
#         for sign in self.sign_names:
#             if sign in text_lower:
#                 return sign.title()
        
#         return None
    
#     def extract_effects(self, text: str) -> List[AstrologicalEffect]:
#         """Extract effects from text"""
#         effects = []
#         text_lower = text.lower()
        
#         # Split text around effect indicators
#         for indicator in self.effect_indicators:
#             if indicator in text_lower:
#                 # Get text after the indicator
#                 parts = text_lower.split(indicator, 1)
#                 if len(parts) > 1:
#                     effect_text = parts[1].strip()
                    
#                     # Determine if effect is positive or negative
#                     is_positive = any(pos in effect_text for pos in self.positive_effects)
#                     is_negative = any(neg in effect_text for neg in self.negative_effects)
                    
#                     # Default to positive if unclear
#                     positive = is_positive or not is_negative
                    
#                     # Extract category
#                     category = self.categorize_effect(effect_text)
                    
#                     effect = AstrologicalEffect(
#                         category=category,
#                         description=effect_text[:100],  # Limit description length
#                         positive=positive,
#                         strength="medium"
#                     )
#                     effects.append(effect)
        
#         # If no effects found, create a general one
#         if not effects:
#             effect = AstrologicalEffect(
#                 category="general",
#                 description="General astrological effect",
#                 positive=True
#             )
#             effects.append(effect)
        
#         return effects
    
#     def categorize_effect(self, effect_text: str) -> str:
#         """Categorize the type of effect"""
#         categories = {
#             'wealth': ['money', 'wealth', 'riches', 'prosperity', 'financial'],
#             'health': ['health', 'disease', 'illness', 'medical', 'body'],
#             'marriage': ['marriage', 'spouse', 'partner', 'relationship'],
#             'career': ['career', 'job', 'profession', 'work', 'business'],
#             'education': ['education', 'learning', 'knowledge', 'study'],
#             'spiritual': ['spiritual', 'religious', 'devotion', 'meditation'],
#             'family': ['family', 'children', 'parents', 'siblings'],
#             'travel': ['travel', 'journey', 'foreign', 'abroad']
#         }
        
#         effect_lower = effect_text.lower()
        
#         for category, keywords in categories.items():
#             if any(keyword in effect_lower for keyword in keywords):
#                 return category
        
#         return 'general'
    
#     def extract_conditions(self, text: str) -> AstrologicalCondition:
#         """Extract all conditions from text"""
#         planet = self.extract_planet(text)
#         house = self.extract_house(text)
#         sign = self.extract_sign(text)
        
#         # Look for additional conditions
#         additional = {}
#         text_lower = text.lower()
        
#         # Check for exaltation/debilitation
#         if 'exalted' in text_lower or 'exaltation' in text_lower:
#             additional['exalted'] = True
#         elif 'debilitated' in text_lower or 'debilitation' in text_lower:
#             additional['debilitated'] = True
        
#         # Check for own sign
#         if 'own sign' in text_lower or 'own house' in text_lower:
#             additional['own_sign'] = True
        
#         # Check for aspects
#         if 'aspect' in text_lower:
#             additional['has_aspect'] = True
        
#         return AstrologicalCondition(
#             planet=planet,
#             house=house,
#             sign=sign,
#             additional_conditions=additional if additional else None
#         )
    
#     def is_valid_rule_sentence(self, sentence: str) -> bool:
#         """Check if a sentence contains a valid astrological rule"""
#         # Must have a planet
#         if not self.extract_planet(sentence):
#             return False
        
#         # Must have either house or sign
#         house = self.extract_house(sentence)
#         sign = self.extract_sign(sentence)
        
#         if not house and not sign:
#             return False
        
#         # Must have an effect indicator
#         text_lower = sentence.lower()
#         has_effect = any(indicator in text_lower for indicator in self.effect_indicators)
        
#         return has_effect
    
#     def extract_rule_from_sentence(self, sentence: str, source_info: SourceInfo) -> Optional[AstrologicalRule]:
#         """Extract a complete rule from a single sentence"""
        
#         # Enhanced rule extraction for classical texts
#         rule = self.extract_classical_rule(sentence, source_info)
#         if rule:
#             return rule
        
#         if not self.is_valid_rule_sentence(sentence):
#             return None
        
#         try:
#             conditions = self.extract_conditions(sentence)
#             effects = self.extract_effects(sentence)
            
#             # Generate tags based on content
#             tags = []
#             if conditions.planet:
#                 tags.append(f"planet:{conditions.planet.lower()}")
#             if conditions.house:
#                 tags.append(f"house:{conditions.house}")
#             if conditions.sign:
#                 tags.append(f"sign:{conditions.sign.lower()}")
            
#             for effect in effects:
#                 tags.append(f"category:{effect.category}")
#                 if not effect.positive:
#                     tags.append("negative")
            
#             rule = AstrologicalRule(
#                 id="",  # Will be auto-generated
#                 original_text=sentence.strip(),
#                 conditions=conditions,
#                 effects=effects,
#                 source=source_info,
#                 tags=tags,
#                 confidence_score=self.calculate_confidence(sentence, conditions, effects)
#             )
            
#             return rule
            
#         except Exception as e:
#             print(f"Error extracting rule from sentence: {e}")
#             return None
    
#     def extract_classical_rule(self, sentence: str, source_info: SourceInfo) -> Optional[AstrologicalRule]:
#         """Enhanced rule extraction for classical texts like BPHS"""
        
#         sentence_lower = sentence.lower()
        
#         # Pattern 1: "Mars in 7th indicates Kuja Dosha"
#         planet_house_pattern = re.search(
#             r'(sun|moon|mars|mercury|jupiter|venus|saturn|rahu|ketu|mangal|budh|shukra|shani|surya|chandra)\s*(?:in\s*(?:the\s*)?(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)?)\s*(?:indicates?|signifies?|causes?|gives?|means?|will)\s*([^.]{5,100})',
#             sentence_lower
#         )
        
#         if planet_house_pattern:
#             planet = self.normalize_planet_name(planet_house_pattern.group(1))
#             house = int(planet_house_pattern.group(2)) if planet_house_pattern.group(2) else None
#             effect_text = planet_house_pattern.group(3).strip()
            
#             return self.create_classical_rule(sentence, planet, house, None, effect_text, source_info, 0.9)
        
#         # Pattern 2: "7th lord in 6th means spouse becomes enemy"
#         lord_placement_pattern = re.search(
#             r'(?:lord\s*of\s*(?:the\s*)?)?(\d+)(?:st|nd|rd|th)?\s*(?:house\s*)?lord\s*(?:in\s*(?:the\s*)?(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)?)\s*(?:indicates?|means?|causes?|will)\s*([^.]{5,100})',
#             sentence_lower
#         )
        
#         if lord_placement_pattern:
#             source_house = lord_placement_pattern.group(1)
#             target_house = int(lord_placement_pattern.group(2)) if lord_placement_pattern.group(2) else None
#             effect_text = lord_placement_pattern.group(3).strip()
            
#             return self.create_classical_rule(sentence, f"{source_house}th lord", target_house, None, effect_text, source_info, 0.88)
        
#         # Pattern 3: "Placement of Mars in 7th..."
#         placement_pattern = re.search(
#             r'placement\s*of\s*(sun|moon|mars|mercury|jupiter|venus|saturn|rahu|ketu|mangal|budh|shukra|shani|surya|chandra)\s*(?:in\s*(?:the\s*)?(\d+)(?:st|nd|rd|th)?\s*(?:house|bhava)?)\s*(?:indicates?|signifies?|causes?|gives?|means?|will)\s*([^.]{5,100})',
#             sentence_lower
#         )
        
#         if placement_pattern:
#             planet = self.normalize_planet_name(placement_pattern.group(1))
#             house = int(placement_pattern.group(2)) if placement_pattern.group(2) else None
#             effect_text = placement_pattern.group(3).strip()
            
#             return self.create_classical_rule(sentence, planet, house, None, effect_text, source_info, 0.87)
        
#         # Pattern 4: Yoga detection
#         yoga_pattern = re.search(
#             r'(kuja\s*dosha|rajyoga|raj\s*yoga|dharmakarmadipati\s*yoga|brahma\s*yoga|[a-z]+\s*dosha|[a-z]+\s*yoga)',
#             sentence_lower
#         )
        
#         if yoga_pattern:
#             yoga_name = yoga_pattern.group(1)
#             # Try to find associated planet
#             planet_in_yoga = None
#             for planet in self.planet_names:
#                 if planet in sentence_lower:
#                     planet_in_yoga = self.normalize_planet_name(planet)
#                     break
            
#             return self.create_classical_rule(sentence, planet_in_yoga, None, None, yoga_name, source_info, 0.85)
        
#         return None
    
#     def normalize_planet_name(self, planet: str) -> str:
#         """Normalize planet names from Sanskrit/Hindi to English"""
#         planet_map = {
#             'surya': 'Sun',
#             'chandra': 'Moon', 
#             'mangal': 'Mars',
#             'budh': 'Mercury',
#             'brihaspati': 'Jupiter',
#             'guru': 'Jupiter',
#             'shukra': 'Venus',
#             'shani': 'Saturn'
#         }
        
#         planet_lower = planet.lower()
#         return planet_map.get(planet_lower, planet.title())
    
#     def create_classical_rule(self, sentence: str, planet: str, house: int, sign: str, 
#                             effect_text: str, source_info: SourceInfo, confidence: float) -> AstrologicalRule:
#         """Create a rule from classical text extraction"""
        
#         conditions = AstrologicalCondition(
#             planet=planet,
#             house=house,
#             sign=sign
#         )
        
#         effects = [AstrologicalEffect(
#             category=self.categorize_effect(effect_text),
#             description=effect_text[:100],
#             positive=not any(neg in effect_text.lower() for neg in ['conflict', 'trouble', 'problem', 'disease', 'death', 'enemy'])
#         )]
        
#         tags = []
#         if planet:
#             tags.append(f"planet:{planet.lower()}")
#         if house:
#             tags.append(f"house:{house}")
#         if 'dosha' in effect_text.lower():
#             tags.append("dosha")
#         if 'yoga' in effect_text.lower():
#             tags.append("yoga")
        
#         return AstrologicalRule(
#             id="",
#             original_text=sentence.strip(),
#             conditions=conditions,
#             effects=effects,
#             source=source_info,
#             tags=tags,
#             confidence_score=confidence
#         )
    
#     def calculate_confidence(self, sentence: str, conditions: AstrologicalCondition, 
#                            effects: List[AstrologicalEffect]) -> float:
#         """Calculate confidence score for extracted rule"""
#         confidence = 0.5  # Base confidence
        
#         # Increase confidence for specific conditions
#         if conditions.planet:
#             confidence += 0.2
#         if conditions.house:
#             confidence += 0.15
#         if conditions.sign:
#             confidence += 0.1
        
#         # Increase confidence for clear effects
#         if len(effects) > 0 and effects[0].description:
#             confidence += 0.1
        
#         # Decrease confidence for very short or very long sentences
#         sentence_length = len(sentence.split())
#         if sentence_length < 5 or sentence_length > 50:
#             confidence -= 0.1
        
#         return min(1.0, max(0.1, confidence))
    
#     def extract_rules_from_sentences(self, sentences: List[str], 
#                                    source_info: SourceInfo) -> List[AstrologicalRule]:
#         """Extract rules from a list of sentences"""
        
#         rules = []
        
#         for sentence in sentences:
#             rule = self.extract_rule_from_sentence(sentence, source_info)
#             if rule:
#                 rules.append(rule)
        
#         return rules
    
#     def extract_rules_batch(self, sentence_groups: List[Tuple[List[str], SourceInfo]]) -> List[AstrologicalRule]:
#         """Extract rules from multiple documents/sources"""
        
#         all_rules = []
        
#         for sentences, source_info in sentence_groups:
#             rules = self.extract_rules_from_sentences(sentences, source_info)
#             all_rules.extend(rules)
            
#             print(f"Extracted {len(rules)} rules from {source_info.title}")
        
#         return all_rules


# # Utility functions for testing and debugging

# def demo_rule_extraction():
#     """Demo function to test rule extraction"""
    
#     extractor = RuleExtractor()
    
#     # Test sentences
#     test_sentences = [
#         "Mars in the 7th house causes conflicts in marriage",
#         "Jupiter in its own sign gives wisdom and prosperity",
#         "Sun in the 10th house brings success in career",
#         "Moon in Cancer indicates emotional nature",
#         "Saturn in the 12th house leads to spiritual growth but causes delays",
#         "Venus exalted in Pisces gives artistic talents"
#     ]
    
#     source = SourceInfo(
#         title="Test Astrology Book",
#         author="Test Author",
#         authority_level=AuthorityLevel.TRADITIONAL
#     )
    
#     print("🧪 Testing Rule Extraction")
#     print("=" * 40)
    
#     for i, sentence in enumerate(test_sentences, 1):
#         print(f"\n{i}. Input: {sentence}")
        
#         rule = extractor.extract_rule_from_sentence(sentence, source)
        
#         if rule:
#             print(f"   ✅ Planet: {rule.conditions.planet}")
#             print(f"   ✅ House: {rule.conditions.house}")
#             print(f"   ✅ Sign: {rule.conditions.sign}")
#             print(f"   ✅ Effects: {len(rule.effects)}")
#             print(f"   ✅ Confidence: {rule.confidence_score:.2f}")
#             print(f"   ✅ Tags: {', '.join(rule.tags)}")
#         else:
#             print("   ❌ No rule extracted")


# if __name__ == "__main__":
#     demo_rule_extraction()