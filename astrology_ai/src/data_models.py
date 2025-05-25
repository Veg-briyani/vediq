# src/data_models.py
"""
Data models for the Astrology AI system
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class PlanetName(Enum):
    """Standard planet names"""
    SUN = "Sun"
    MOON = "Moon"
    MARS = "Mars"
    MERCURY = "Mercury"
    JUPITER = "Jupiter"
    VENUS = "Venus"
    SATURN = "Saturn"
    RAHU = "Rahu"
    KETU = "Ketu"


class ZodiacSign(Enum):
    """Zodiac signs"""
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"


class AuthorityLevel(Enum):
    """Source authority levels"""
    CLASSICAL = 1  # Ancient classical texts
    TRADITIONAL = 2  # Traditional authors
    MODERN = 3  # Modern interpretations
    COMMENTARY = 4  # Commentaries and interpretations


@dataclass
class SourceInfo:
    """Information about the source of a rule"""
    title: str
    author: Optional[str] = None
    page_number: Optional[int] = None
    chapter: Optional[str] = None
    authority_level: AuthorityLevel = AuthorityLevel.MODERN
    publication_year: Optional[int] = None


@dataclass
class AstrologicalCondition:
    """Represents a condition in an astrological rule"""
    planet: Optional[str] = None
    house: Optional[int] = None
    sign: Optional[str] = None
    nakshatra: Optional[str] = None
    aspect: Optional[str] = None
    conjunction: Optional[List[str]] = None
    degree_range: Optional[tuple] = None
    additional_conditions: Optional[Dict[str, Any]] = None


@dataclass
class AstrologicalEffect:
    """Represents an effect or result"""
    category: str  # e.g., "health", "wealth", "marriage", "career"
    description: str
    positive: bool = True
    strength: str = "medium"  # weak, medium, strong
    timing: Optional[str] = None  # immediate, delayed, etc.


@dataclass
class AstrologicalRule:
    """Core data structure for storing astrological rules"""
    id: str
    original_text: str
    conditions: AstrologicalCondition
    effects: List[AstrologicalEffect]
    source: SourceInfo
    tags: List[str] = field(default_factory=list)
    confidence_score: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Validation after initialization"""
        if not self.id:
            # Generate ID based on content hash if not provided
            import hashlib
            content = f"{self.original_text}{self.source.title}"
            self.id = hashlib.md5(content.encode()).hexdigest()[:12]


@dataclass
class PlanetaryPosition:
    """Position of a planet in a chart"""
    planet: str
    sign: str
    house: int
    degree: float
    nakshatra: Optional[str] = None
    nakshatra_pada: Optional[int] = None
    retrograde: bool = False


@dataclass
class HouseInfo:
    """Information about a house in the chart"""
    house_number: int
    sign: str
    house_lord: str
    planets_in_house: List[str] = field(default_factory=list)
    aspects_received: List[str] = field(default_factory=list)


@dataclass
class BirthChart:
    """Complete birth chart data"""
    birth_datetime: datetime
    latitude: float
    longitude: float
    timezone: str
    planetary_positions: Dict[str, PlanetaryPosition] = field(default_factory=dict)
    houses: Dict[int, HouseInfo] = field(default_factory=dict)
    ascendant: Optional[str] = None
    chart_type: str = "D-1"  # D-1, D-9, D-10, etc.
    ayanamsa: Optional[str] = None
    
    def get_planet_in_house(self, house_number: int) -> List[str]:
        """Get all planets in a specific house"""
        planets = []
        for planet, position in self.planetary_positions.items():
            if position.house == house_number:
                planets.append(planet)
        return planets
    
    def get_planet_position(self, planet: str) -> Optional[PlanetaryPosition]:
        """Get position of a specific planet"""
        return self.planetary_positions.get(planet)


@dataclass
class RuleMatch:
    """Represents a matched rule for chart interpretation"""
    rule: AstrologicalRule
    match_strength: float  # 0.0 to 1.0
    matched_conditions: Dict[str, Any]
    applicable_effects: List[AstrologicalEffect]
    explanation: str
    
    def __lt__(self, other):
        """Enable sorting by match strength"""
        return self.match_strength < other.match_strength


@dataclass
class ChartInterpretation:
    """Complete interpretation of a birth chart"""
    chart: BirthChart
    matched_rules: List[RuleMatch]
    overall_summary: str
    category_summaries: Dict[str, str] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.now)
    confidence_level: str = "medium"
    
    def get_rules_by_category(self, category: str) -> List[RuleMatch]:
        """Get all rule matches for a specific category"""
        return [
            match for match in self.matched_rules
            if any(effect.category == category for effect in match.applicable_effects)
        ]


# Utility functions for working with data models

def create_simple_rule(text: str, source_title: str, planet: str = None, 
                      house: int = None, effect_desc: str = None) -> AstrologicalRule:
    """Helper function to create a simple rule"""
    
    condition = AstrologicalCondition(planet=planet, house=house)
    effect = AstrologicalEffect(
        category="general",
        description=effect_desc or "General effect",
        positive=True
    )
    source = SourceInfo(title=source_title)
    
    return AstrologicalRule(
        id="",  # Will be auto-generated
        original_text=text,
        conditions=condition,
        effects=[effect],
        source=source
    )


def validate_rule(rule: AstrologicalRule) -> List[str]:
    """Validate a rule and return any errors"""
    errors = []
    
    if not rule.original_text.strip():
        errors.append("Original text cannot be empty")
    
    if not rule.source.title.strip():
        errors.append("Source title is required")
    
    if not rule.effects:
        errors.append("At least one effect is required")
    
    # Check if conditions make sense
    if rule.conditions.house and not (1 <= rule.conditions.house <= 12):
        errors.append("House number must be between 1 and 12")
    
    return errors