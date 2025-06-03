# src/knowledge_base.py
"""
Knowledge base system for storing and retrieving astrological rules
"""

import json
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from .data_models import AstrologicalRule, AstrologicalCondition, SourceInfo, AuthorityLevel

# Import configuration system
import sys
config_path = Path(__file__).parent.parent / "config"
sys.path.insert(0, str(config_path))

try:
    from settings import get_config, get_database_path, get_export_path
except ImportError:
    # Fallback for when config system is not available
    def get_database_path(db_type: str = "main") -> Path:
        return Path("data/astrology_rules.db")
    
    def get_export_path(filename: str) -> Path:
        return Path("data") / filename


class KnowledgeBase:
    """
    Manages storage and retrieval of astrological rules
    Uses centralized configuration for all file paths
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize knowledge base with optional custom database path
        
        Args:
            db_path: Custom database path (optional, uses config if not provided)
        """
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = str(get_database_path())
        
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        
        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS rules (
                    id TEXT PRIMARY KEY,
                    original_text TEXT NOT NULL,
                    planet TEXT,
                    house INTEGER,
                    sign TEXT,
                    nakshatra TEXT,
                    conditions_json TEXT,
                    effects_json TEXT NOT NULL,
                    source_title TEXT NOT NULL,
                    source_author TEXT,
                    source_page INTEGER,
                    authority_level INTEGER,
                    tags_json TEXT,
                    confidence_score REAL DEFAULT 0.5,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_rules_planet ON rules(planet);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_rules_house ON rules(house);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_rules_sign ON rules(sign);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_rules_source ON rules(source_title);
            """)
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS astrological_rules (
                    id TEXT PRIMARY KEY,
                    original_text TEXT NOT NULL,
                    
                    -- Conditions
                    planet TEXT,
                    house INTEGER,
                    sign TEXT,
                    aspect TEXT,
                    strength TEXT,
                    
                    -- Effects (JSON array)
                    effects TEXT,
                    
                    -- Source information
                    source_title TEXT,
                    source_author TEXT,
                    authority_level INTEGER,
                    page_number INTEGER,
                    
                    -- Metadata
                    confidence_score REAL,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    -- Search indexes
                    search_text TEXT -- For full-text search
                )
            ''')
            
            conn.execute('CREATE INDEX IF NOT EXISTS idx_planet ON astrological_rules(planet)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_house ON astrological_rules(house)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_sign ON astrological_rules(sign)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_authority ON astrological_rules(authority_level)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_confidence ON astrological_rules(confidence_score)')
            
            conn.execute('''
                CREATE VIRTUAL TABLE IF NOT EXISTS rules_fts USING fts5(
                    id, original_text, search_text, content='astrological_rules'
                )
            ''')
            
            conn.commit()
    
    def serialize_rule(self, rule: AstrologicalRule) -> Dict[str, Any]:
        """Convert rule object to database-ready format"""
        
        # Extract main condition fields for indexing
        planet = rule.conditions.planet
        house = rule.conditions.house
        sign = rule.conditions.sign
        nakshatra = rule.conditions.nakshatra
        
        # Serialize complex fields to JSON
        conditions_json = json.dumps({
            'planet': rule.conditions.planet,
            'house': rule.conditions.house,
            'sign': rule.conditions.sign,
            'nakshatra': rule.conditions.nakshatra,
            'aspect': rule.conditions.aspect,
            'conjunction': rule.conditions.conjunction,
            'degree_range': rule.conditions.degree_range,
            'additional_conditions': rule.conditions.additional_conditions
        })
        
        effects_json = json.dumps([
            {
                'category': effect.category,
                'description': effect.description,
                'positive': effect.positive,
                'strength': effect.strength,
                'timing': effect.timing
            }
            for effect in rule.effects
        ])
        
        tags_json = json.dumps(rule.tags)
        
        return {
            'id': rule.id,
            'original_text': rule.original_text,
            'planet': planet,
            'house': house,
            'sign': sign,
            'nakshatra': nakshatra,
            'conditions_json': conditions_json,
            'effects_json': effects_json,
            'source_title': rule.source.title,
            'source_author': rule.source.author,
            'source_page': rule.source.page_number,
            'authority_level': rule.source.authority_level.value,
            'tags_json': tags_json,
            'confidence_score': rule.confidence_score,
            'created_at': rule.created_at.isoformat(),
            'updated_at': rule.updated_at.isoformat() if rule.updated_at else None
        }
    
    def deserialize_rule(self, row: sqlite3.Row) -> AstrologicalRule:
        """Convert database row back to rule object"""
        
        # Parse JSON fields
        conditions_data = json.loads(row['conditions_json'])
        effects_data = json.loads(row['effects_json'])
        tags = json.loads(row['tags_json'])
        
        # Reconstruct condition object
        from .data_models import AstrologicalCondition, AstrologicalEffect
        
        condition = AstrologicalCondition(
            planet=conditions_data.get('planet'),
            house=conditions_data.get('house'),
            sign=conditions_data.get('sign'),
            nakshatra=conditions_data.get('nakshatra'),
            aspect=conditions_data.get('aspect'),
            conjunction=conditions_data.get('conjunction'),
            degree_range=conditions_data.get('degree_range'),
            additional_conditions=conditions_data.get('additional_conditions')
        )
        
        # Reconstruct effects
        effects = [
            AstrologicalEffect(
                category=effect_data['category'],
                description=effect_data['description'],
                positive=effect_data['positive'],
                strength=effect_data['strength'],
                timing=effect_data.get('timing')
            )
            for effect_data in effects_data
        ]
        
        # Reconstruct source
        source = SourceInfo(
            title=row['source_title'],
            author=row['source_author'],
            page_number=row['source_page'],
            authority_level=AuthorityLevel(row['authority_level'])
        )
        
        # Reconstruct rule
        return AstrologicalRule(
            id=row['id'],
            original_text=row['original_text'],
            conditions=condition,
            effects=effects,
            source=source,
            tags=tags,
            confidence_score=row['confidence_score'],
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )
    
    def store_rule(self, rule: AstrologicalRule) -> bool:
        """Store a single rule in the database"""
        
        try:
            data = self.serialize_rule(rule)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO rules 
                    (  planet, house, sign, nakshatra, 
                     conditions_json, effects_json, source_title, source_author, 
                     source_page, authority_level, tags_json, confidence_score, 
                     created_at, updated_at)
                    VALUES 
                    (:id, :original_text, :planet, :house, :sign, :nakshatra,
                     :conditions_json, :effects_json, :source_title, :source_author,
                     :source_page, :authority_level, :tags_json, :confidence_score,
                     :created_at, :updated_at)
                """, data)
                conn.commit()
            
            return True
            
        except Exception as e:
            print(f"Error storing rule {rule.id}: {e}")
            return False
    
    def store_rules_batch(self, rules: List[AstrologicalRule]) -> int:
        """Store multiple rules efficiently"""
        
        stored_count = 0
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                for rule in rules:
                    try:
                        data = self.serialize_rule(rule)
                        
                        conn.execute("""
                            INSERT OR REPLACE INTO rules 
                            (id, original_text, planet, house, sign, nakshatra, 
                             conditions_json, effects_json, source_title, source_author, 
                             source_page, authority_level, tags_json, confidence_score, 
                             created_at, updated_at)
                            VALUES 
                            (:id, :original_text, :planet, :house, :sign, :nakshatra,
                             :conditions_json, :effects_json, :source_title, :source_author,
                             :source_page, :authority_level, :tags_json, :confidence_score,
                             :created_at, :updated_at)
                        """, data)
                        
                        stored_count += 1
                        
                    except Exception as e:
                        print(f"Error storing rule {rule.id}: {e}")
                
                conn.commit()
        
        except Exception as e:
            print(f"Batch storage error: {e}")
        
        return stored_count
    
    def get_rule_by_id(self, rule_id: str) -> Optional[AstrologicalRule]:
        """Get a specific rule by ID"""
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM rules WHERE id = ?", (rule_id,))
            row = cursor.fetchone()
            
            if row:
                return self.deserialize_rule(row)
            
            return None
    
    def search_rules(self, planet: str = None, house: int = None, 
                    sign: str = None, source: str = None, 
                    min_confidence: float = 0.0, limit: int = None) -> List[AstrologicalRule]:
        """Search rules by various criteria"""
        
        query = "SELECT * FROM rules WHERE 1=1"
        params = []
        
        if planet:
            query += " AND planet = ?"
            params.append(planet)
        
        if house:
            query += " AND house = ?"
            params.append(house)
        
        if sign:
            query += " AND sign = ?"
            params.append(sign)
        
        if source:
            query += " AND source_title LIKE ?"
            params.append(f"%{source}%")
        
        if min_confidence > 0:
            query += " AND confidence_score >= ?"
            params.append(min_confidence)
        
        query += " ORDER BY confidence_score DESC, authority_level ASC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        rules = []
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            
            for row in cursor:
                rule = self.deserialize_rule(row)
                rules.append(rule)
        
        return rules
    
    def get_rules_by_tag(self, tag: str) -> List[AstrologicalRule]:
        """Get all rules containing a specific tag"""
        
        rules = []
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM rules")
            
            for row in cursor:
                tags = json.loads(row['tags_json'])
                if tag in tags:
                    rule = self.deserialize_rule(row)
                    rules.append(rule)
        
        return rules
    
    def get_conflicting_rules(self, rule: AstrologicalRule) -> List[AstrologicalRule]:
        """Find rules that might conflict with the given rule"""
        
        # Find rules with same conditions but different effects
        matching_rules = self.search_rules(
            planet=rule.conditions.planet,
            house=rule.conditions.house,
            sign=rule.conditions.sign
        )
        
        conflicts = []
        
        for other_rule in matching_rules:
            if other_rule.id != rule.id:
                # Check if effects are contradictory
                for effect in rule.effects:
                    for other_effect in other_rule.effects:
                        if (effect.category == other_effect.category and 
                            effect.positive != other_effect.positive):
                            conflicts.append(other_rule)
                            break
        
        return conflicts
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) as total_rules FROM rules")
            total_rules = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(DISTINCT source_title) as unique_sources FROM rules")
            unique_sources = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT planet, COUNT(*) as count FROM rules WHERE planet IS NOT NULL GROUP BY planet ORDER BY count DESC")
            planet_counts = dict(cursor.fetchall())
            
            cursor = conn.execute("SELECT house, COUNT(*) as count FROM rules WHERE house IS NOT NULL GROUP BY house ORDER BY house")
            house_counts = dict(cursor.fetchall())
            
            cursor = conn.execute("SELECT AVG(confidence_score) as avg_confidence FROM rules")
            avg_confidence = cursor.fetchone()[0]
        
        return {
            'total_rules': total_rules,
            'unique_sources': unique_sources,
            'planet_distribution': planet_counts,
            'house_distribution': house_counts,
            'average_confidence': round(avg_confidence, 3) if avg_confidence else 0
        }
    
    def export_rules_json(self, output_path: str = None):
        """Export all rules to JSON format using configuration paths"""
        
        if output_path is None:
            try:
                output_path = str(get_export_path("rules_export.json"))
            except:
                output_path = "data/rules_export.json"
        
        # Ensure export directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Query the correct table where data is actually stored
            cursor = conn.execute('''
                SELECT id, original_text, planet, house, sign, nakshatra,
                       conditions_json, effects_json, source_title, source_author,
                       source_page, authority_level, tags_json, confidence_score,
                       created_at, updated_at
                FROM rules 
                ORDER BY confidence_score DESC, authority_level ASC
            ''')
            
            rules = []
            for row in cursor:
                rule_dict = dict(row)
                
                # Parse JSON fields
                try:
                    if rule_dict['conditions_json']:
                        rule_dict['conditions'] = json.loads(rule_dict['conditions_json'])
                    else:
                        rule_dict['conditions'] = {}
                    
                    if rule_dict['effects_json']:
                        rule_dict['effects'] = json.loads(rule_dict['effects_json'])
                    else:
                        rule_dict['effects'] = []
                    
                    if rule_dict['tags_json']:
                        rule_dict['tags'] = json.loads(rule_dict['tags_json'])
                    else:
                        rule_dict['tags'] = []
                    
                    # Remove the raw JSON fields for cleaner output
                    del rule_dict['conditions_json']
                    del rule_dict['effects_json'] 
                    del rule_dict['tags_json']
                    
                except json.JSONDecodeError as e:
                    print(f"Warning: Error parsing JSON for rule {rule_dict['id']}: {e}")
                    rule_dict['conditions'] = {}
                    rule_dict['effects'] = []
                    rule_dict['tags'] = []
                
                rules.append(rule_dict)
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'total_rules': len(rules),
            'database_path': self.db_path,
            'export_info': {
                'source': 'Astrology AI Knowledge Base',
                'table': 'rules',
                'version': '1.0.0'
            },
            'rules': rules
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return output_path


# Demo and testing functions

def demo_knowledge_base():
    """Demo the knowledge base functionality"""
    
    from .rule_extractor import RuleExtractor
    
    # Create a test knowledge base
    kb = KnowledgeBase("data/test_astrology.db")
    
    # Create some test rules
    extractor = RuleExtractor()
    source = SourceInfo(title="Demo Astrology Book", authority_level=AuthorityLevel.TRADITIONAL)
    
    test_sentences = [
        "Mars in the 7th house causes conflicts in marriage",
        "Jupiter in its own sign gives wisdom and prosperity",
        "Sun in the 10th house brings success in career"
    ]
    
    # Extract and store rules
    rules = extractor.extract_rules_from_sentences(test_sentences, source)
    stored_count = kb.store_rules_batch(rules)
    
    print(f"✅ Stored {stored_count} rules")
    
    # Test searches
    print(f"\n🔍 Mars rules: {len(kb.search_rules(planet='Mars'))}")
    print(f"🔍 7th house rules: {len(kb.search_rules(house=7))}")
    print(f"🔍 High confidence rules: {len(kb.search_rules(min_confidence=0.7))}")
    
    # Show stats
    stats = kb.get_database_stats()
    print(f"\n📊 Database stats: {stats}")


if __name__ == "__main__":
    demo_knowledge_base()