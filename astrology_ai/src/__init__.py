# src/__init__.py
"""
Astrology AI - Phase 1: Foundation & Rule Extraction System

A system for extracting structured astrological rules from classical texts
and building an intelligent knowledge base.
"""

__version__ = "1.0.0"
__author__ = "Astrology AI Project"

# Core components
from .data_models import (
    AstrologicalRule,
    AstrologicalCondition, 
    AstrologicalEffect,
    SourceInfo,
    BirthChart,
    PlanetaryPosition,
    AuthorityLevel
)

from .document_processor import DocumentProcessor
from .rule_extractor import RuleExtractor  
from .knowledge_base import KnowledgeBase

# Configuration system
import sys
from pathlib import Path

# Add config to path for imports
config_path = Path(__file__).parent.parent / "config"
sys.path.insert(0, str(config_path))

try:
    from settings import get_config, get_database_path
except ImportError:
    # Fallback for when config system is not available
    def get_database_path(db_type: str = "main") -> Path:
        return Path("data/astrology_rules.db")
    
    class MockConfig:
        def __init__(self):
            self.directories = type('obj', (object,), {
                'books_dir': Path("data/books"),
                'rules_dir': Path("data/rules"),
                'exports_dir': Path("data/exports")
            })()
    
    def get_config():
        return MockConfig()

# Utility functions
def get_version():
    """Get the current version of Astrology AI"""
    return __version__

def create_demo_system():
    """Create a demo system with sample data"""
    from .data_models import create_simple_rule
    
    # Initialize components with configuration
    config = get_config()
    processor = DocumentProcessor()
    extractor = RuleExtractor()
    kb = KnowledgeBase(str(get_database_path()))
    
    # Create some demo rules
    demo_rules = [
        create_simple_rule(
            "Mars in the 7th house causes conflicts in marriage",
            "Classical Astrology Text",
            planet="Mars",
            house=7,
            effect_desc="conflicts in marriage"
        ),
        create_simple_rule(
            "Jupiter in its own sign gives wisdom and prosperity",
            "Classical Astrology Text", 
            planet="Jupiter",
            effect_desc="wisdom and prosperity"
        )
    ]
    
    # Store demo rules
    kb.store_rules_batch(demo_rules)
    
    return {
        'processor': processor,
        'extractor': extractor,
        'knowledge_base': kb,
        'demo_rules_count': len(demo_rules)
    }

# Main system class for easy access
class AstrologyAI:
    """
    Main interface for the Astrology AI system
    Uses centralized configuration for all paths and settings
    """
    
    def __init__(self, db_path: str = None, config_file: str = None):
        """
        Initialize AstrologyAI with optional custom database path
        
        Args:
            db_path: Custom database path (optional, uses config if not provided)
            config_file: Custom configuration file (optional)
        """
        # Initialize configuration
        if config_file:
            # Import here to avoid circular imports
            from settings import AstrologyAIConfig
            self.config = AstrologyAIConfig(config_file)
        else:
            self.config = get_config()
        
        # Use provided db_path or get from configuration
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = str(get_database_path())
        
        # Initialize components
        self.processor = DocumentProcessor()
        self.extractor = RuleExtractor()
        self.knowledge_base = KnowledgeBase(self.db_path)
    
    def process_book(self, pdf_path: str, source_title: str, 
                    author: str = None, authority_level: AuthorityLevel = AuthorityLevel.MODERN):
        """Complete pipeline: PDF -> Rules -> Storage"""
        
        # Process PDF
        doc_result = self.processor.process_document(pdf_path)
        
        # Create source info
        source_info = SourceInfo(
            title=source_title,
            author=author,
            authority_level=authority_level
        )
        
        # Extract rules
        rules = self.extractor.extract_rules_from_sentences(
            doc_result.astrological_sentences,
            source_info
        )
        
        # Store rules
        stored_count = self.knowledge_base.store_rules_batch(rules)
        
        return {
            'document': doc_result.filename,
            'sentences_extracted': len(doc_result.astrological_sentences),
            'rules_extracted': len(rules),
            'rules_stored': stored_count
        }
    
    def search_rules(self, **criteria):
        """Search for rules using various criteria"""
        return self.knowledge_base.search_rules(**criteria)
    
    def get_stats(self):
        """Get system statistics"""
        return self.knowledge_base.get_database_stats()
    
    def get_configuration_info(self):
        """Get information about current configuration"""
        return {
            'database_path': self.db_path,
            'books_directory': str(self.config.directories.books_dir),
            'rules_directory': str(self.config.directories.rules_dir),
            'exports_directory': str(self.config.directories.exports_dir),
            'project_root': str(self.config.directories.project_root)
        }
    
    def validate_setup(self):
        """Validate system setup and configuration"""
        return self.config.validate_setup()

__all__ = [
    'AstrologyAI',
    'DocumentProcessor',
    'RuleExtractor', 
    'KnowledgeBase',
    'AstrologicalRule',
    'AstrologicalCondition',
    'AstrologicalEffect',
    'SourceInfo',
    'AuthorityLevel',
    'get_version',
    'create_demo_system',
    'get_config',
    'get_database_path'
]