"""
Source Management System for Astrology AI

Manages the hierarchy and authority levels of astrological sources
as defined in config/sources.yaml. Handles source validation,
authority weighting, and conflict resolution.
"""

import yaml
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

# Import configuration
import sys
config_path = Path(__file__).parent.parent / "config"
sys.path.insert(0, str(config_path))

try:
    from settings import get_config
except ImportError:
    def get_config():
        return None

from data_models import AuthorityLevel, SourceInfo


@dataclass
class SourceMetadata:
    """Detailed metadata for an astrological source"""
    title: str
    author: str
    authority_level: int
    language: str
    period: str
    description: str
    priority_score: int = 0
    
    def to_source_info(self) -> SourceInfo:
        """Convert to SourceInfo data model"""
        authority_map = {
            1: AuthorityLevel.CLASSICAL,
            2: AuthorityLevel.TRADITIONAL,
            3: AuthorityLevel.MODERN,
            4: AuthorityLevel.COMMENTARY
        }
        
        return SourceInfo(
            title=self.title,
            author=self.author,
            authority_level=authority_map.get(self.authority_level, AuthorityLevel.MODERN)
        )


class SourceManager:
    """
    Manages astrological source hierarchy and authority levels
    """
    
    def __init__(self, sources_file: str = None):
        """
        Initialize source manager
        
        Args:
            sources_file: Path to sources.yaml file (optional, uses config if not provided)
        """
        self.config = get_config()
        
        if sources_file:
            self.sources_file = Path(sources_file)
        else:
            # Use configured path or fallback
            if self.config:
                self.sources_file = self.config.directories.config_dir / "sources.yaml"
            else:
                self.sources_file = Path("config/sources.yaml")
        
        self.sources_data = self._load_sources_config()
        self.source_metadata = self._parse_sources()
    
    def _load_sources_config(self) -> Dict[str, Any]:
        """Load sources configuration from YAML file"""
        
        if not self.sources_file.exists():
            print(f"⚠️  Sources file not found: {self.sources_file}")
            return self._get_default_config()
        
        try:
            with open(self.sources_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"❌ Error loading sources config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default sources configuration"""
        return {
            'classical_sources': [
                {
                    'title': 'Brihat Parashara Hora Shastra',
                    'author': 'Maharishi Parashara',
                    'authority_level': 1,
                    'language': 'Sanskrit',
                    'period': 'Ancient',
                    'description': 'Foundational classical text'
                }
            ],
            'traditional_sources': [],
            'modern_sources': [],
            'source_priority': {
                'classical': 10,
                'traditional': 7,
                'modern': 5,
                'commentary': 3
            },
            'conflict_resolution': {
                'prefer_higher_authority': True,
                'classical_bonus': 0.3,
                'traditional_bonus': 0.2,
                'modern_bonus': 0.1
            }
        }
    
    def _parse_sources(self) -> Dict[str, SourceMetadata]:
        """Parse sources configuration into metadata objects"""
        
        metadata = {}
        priority_map = self.sources_data.get('source_priority', {})
        
        # Process each source category
        for category in ['classical_sources', 'traditional_sources', 'modern_sources']:
            sources = self.sources_data.get(category, [])
            category_name = category.replace('_sources', '')
            priority = priority_map.get(category_name, 5)
            
            for source in sources:
                source_meta = SourceMetadata(
                    title=source.get('title', ''),
                    author=source.get('author', ''),
                    authority_level=source.get('authority_level', 3),
                    language=source.get('language', 'Unknown'),
                    period=source.get('period', 'Unknown'),
                    description=source.get('description', ''),
                    priority_score=priority
                )
                
                metadata[source_meta.title] = source_meta
        
        return metadata
    
    def get_source_by_title(self, title: str) -> Optional[SourceMetadata]:
        """Get source metadata by title"""
        return self.source_metadata.get(title)
    
    def get_sources_by_authority(self, authority_level: int) -> List[SourceMetadata]:
        """Get all sources with specific authority level"""
        return [
            source for source in self.source_metadata.values()
            if source.authority_level == authority_level
        ]
    
    def get_classical_sources(self) -> List[SourceMetadata]:
        """Get all classical sources (authority level 1)"""
        return self.get_sources_by_authority(1)
    
    def get_traditional_sources(self) -> List[SourceMetadata]:
        """Get all traditional sources (authority level 2)"""
        return self.get_sources_by_authority(2)
    
    def get_modern_sources(self) -> List[SourceMetadata]:
        """Get all modern sources (authority level 3)"""
        return self.get_sources_by_authority(3)
    
    def validate_source(self, title: str, author: str = None) -> bool:
        """Validate if a source exists in the hierarchy"""
        source = self.get_source_by_title(title)
        if not source:
            return False
        
        if author and source.author.lower() != author.lower():
            return False
        
        return True
    
    def get_authority_bonus(self, authority_level: int) -> float:
        """Get confidence bonus for authority level"""
        
        conflict_res = self.sources_data.get('conflict_resolution', {})
        
        bonuses = {
            1: conflict_res.get('classical_bonus', 0.3),
            2: conflict_res.get('traditional_bonus', 0.2),
            3: conflict_res.get('modern_bonus', 0.1),
            4: 0.0  # Commentary gets no bonus
        }
        
        return bonuses.get(authority_level, 0.0)
    
    def resolve_source_conflicts(self, sources: List[str]) -> str:
        """Resolve conflicts between multiple sources by authority"""
        
        if not sources:
            return ""
        
        if len(sources) == 1:
            return sources[0]
        
        # Get metadata for all sources
        source_metas = []
        for source_title in sources:
            meta = self.get_source_by_title(source_title)
            if meta:
                source_metas.append(meta)
        
        if not source_metas:
            return sources[0]  # Fallback to first source
        
        # Sort by authority level (lower number = higher authority)
        source_metas.sort(key=lambda x: (x.authority_level, -x.priority_score))
        
        return source_metas[0].title
    
    def get_processing_settings(self) -> Dict[str, Any]:
        """Get processing settings from sources configuration"""
        return self.sources_data.get('processing_settings', {
            'min_sentence_length': 10,
            'max_sentence_length': 500,
            'min_confidence_threshold': 0.3,
            'skip_patterns': []
        })
    
    def get_tag_categories(self) -> Dict[str, List[str]]:
        """Get tag categories for rule classification"""
        return self.sources_data.get('tag_categories', {
            'planets': [],
            'houses': [],
            'signs': [],
            'effects': []
        })
    
    def add_source(self, source_meta: SourceMetadata, category: str = "modern") -> bool:
        """Add a new source to the hierarchy"""
        
        # Add to in-memory metadata
        self.source_metadata[source_meta.title] = source_meta
        
        # Add to configuration data
        category_key = f"{category}_sources"
        if category_key not in self.sources_data:
            self.sources_data[category_key] = []
        
        source_dict = {
            'title': source_meta.title,
            'author': source_meta.author,
            'authority_level': source_meta.authority_level,
            'language': source_meta.language,
            'period': source_meta.period,
            'description': source_meta.description
        }
        
        self.sources_data[category_key].append(source_dict)
        
        return True
    
    def save_sources_config(self) -> bool:
        """Save current sources configuration to file"""
        
        try:
            # Ensure directory exists
            self.sources_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.sources_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.sources_data, f, default_flow_style=False, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Error saving sources config: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about registered sources"""
        
        stats = {
            'total_sources': len(self.source_metadata),
            'by_authority': {},
            'by_language': {},
            'by_period': {}
        }
        
        for source in self.source_metadata.values():
            # By authority level
            auth_level = source.authority_level
            if auth_level not in stats['by_authority']:
                stats['by_authority'][auth_level] = 0
            stats['by_authority'][auth_level] += 1
            
            # By language
            lang = source.language
            if lang not in stats['by_language']:
                stats['by_language'][lang] = 0
            stats['by_language'][lang] += 1
            
            # By period
            period = source.period
            if period not in stats['by_period']:
                stats['by_period'][period] = 0
            stats['by_period'][period] += 1
        
        return stats


def create_source_info(title: str, author: str = None, authority: str = "modern") -> SourceInfo:
    """
    Create SourceInfo from title and authority level
    
    Args:
        title: Source title
        author: Author name (optional)
        authority: Authority level string (classical, traditional, modern, commentary)
        
    Returns:
        SourceInfo object
    """
    
    authority_map = {
        'classical': AuthorityLevel.CLASSICAL,
        'traditional': AuthorityLevel.TRADITIONAL,
        'modern': AuthorityLevel.MODERN,
        'commentary': AuthorityLevel.COMMENTARY
    }
    
    authority_level = authority_map.get(authority.lower(), AuthorityLevel.MODERN)
    
    return SourceInfo(
        title=title,
        author=author,
        authority_level=authority_level
    )


if __name__ == "__main__":
    # Test source manager
    print("📚 Source Management System")
    print("=" * 40)
    
    manager = SourceManager()
    
    print(f"📊 Source Statistics:")
    stats = manager.get_statistics()
    print(f"   Total sources: {stats['total_sources']}")
    print(f"   By authority: {stats['by_authority']}")
    print(f"   By language: {stats['by_language']}")
    
    print(f"\n🏛️  Classical Sources:")
    for source in manager.get_classical_sources():
        print(f"   - {source.title} by {source.author}")
    
    print(f"\n⚙️  Processing Settings:")
    settings = manager.get_processing_settings()
    for key, value in settings.items():
        print(f"   {key}: {value}")
    
    print(f"\n✅ Source management system working!")
