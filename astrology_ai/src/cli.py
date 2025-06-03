# src/cli.py
"""
Complete Command Line Interface for Astrology AI Phase 1
Integrates document processing, rule extraction, and knowledge storage
Uses centralized configuration for all paths and settings
"""

import click
from pathlib import Path
import json
import yaml
from datetime import datetime

# Import configuration system
import sys
config_path = Path(__file__).parent.parent / "config"
sys.path.insert(0, str(config_path))

try:
    from settings import get_config, get_database_path, get_export_path, get_books_dir
except ImportError:
    # Fallback for when config system is not available
    def get_config():
        return None
    def get_database_path(db_type: str = "main"):
        return Path("data/astrology_rules.db")
    def get_export_path(filename: str):
        return Path("data") / filename
    def get_books_dir():
        return Path("data/books")

# Import our modules
from .document_processor import DocumentProcessor
from .rule_extractor import RuleExtractor
from .knowledge_base import KnowledgeBase
from .data_models import SourceInfo, AuthorityLevel


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """🌌 Astrology AI - Ancient Wisdom meets Modern Intelligence
    
    Phase 1: Foundation & Rule Extraction System
    """
    pass


@cli.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--source-title', '-t', help='Title of the source book')
@click.option('--author', '-a', help='Author of the source')
@click.option('--authority', '-l', 
              type=click.Choice(['classical', 'traditional', 'modern', 'commentary']),
              default='modern', help='Authority level of the source')
@click.option('--extract-rules', '-r', is_flag=True, help='Extract rules and store in knowledge base')
@click.option('--show-samples', '-s', is_flag=True, help='Show sample sentences')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
def process_book(pdf_path, source_title, author, authority, extract_rules, show_samples, output):
    """Process an astrology book and optionally extract rules"""
    
    click.echo(f"📚 Processing: {Path(pdf_path).name}")
    
    # Initialize components
    processor = DocumentProcessor()
    
    try:
        # Process the PDF
        result = processor.process_document(pdf_path)
        
        # Display basic results
        click.echo(f"\n📊 Processing Results:")
        click.echo(f"   Document: {result.filename}")
        click.echo(f"   Total sentences: {len(result.sentences)}")
        click.echo(f"   Astrological sentences: {len(result.astrological_sentences)}")
        click.echo(f"   Content ratio: {len(result.astrological_sentences)/len(result.sentences)*100:.1f}%")
        
        if show_samples:
            click.echo(f"\n🔍 Sample astrological sentences:")
            for i, sentence in enumerate(result.astrological_sentences[:5]):
                click.echo(f"   {i+1}. {sentence[:100]}...")
        
        # Extract rules if requested
        if extract_rules:
            click.echo(f"\n🔄 Extracting rules...")
            
            # Create source info
            authority_map = {
                'classical': AuthorityLevel.CLASSICAL,
                'traditional': AuthorityLevel.TRADITIONAL, 
                'modern': AuthorityLevel.MODERN,
                'commentary': AuthorityLevel.COMMENTARY
            }
            
            source_info = SourceInfo(
                title=source_title or result.filename,
                author=author,
                authority_level=authority_map[authority]
            )
            
            # Extract rules
            extractor = RuleExtractor()
            rules = extractor.extract_rules_from_sentences(
                result.astrological_sentences, 
                source_info
            )
            
            click.echo(f"   Extracted {len(rules)} rules")
            
            # Store in knowledge base using configuration
            if rules:
                kb = KnowledgeBase()  # Uses configuration for database path
                stored_count = kb.store_rules_batch(rules)
                click.echo(f"   ✅ Stored {stored_count} rules in knowledge base")
                
                # Show rule samples
                click.echo(f"\n📝 Sample extracted rules:")
                for i, rule in enumerate(rules[:3]):
                    click.echo(f"   {i+1}. {rule.original_text[:80]}...")
                    click.echo(f"      Planet: {rule.conditions.planet}, House: {rule.conditions.house}")
                    click.echo(f"      Effects: {len(rule.effects)}, Confidence: {rule.confidence_score:.2f}")
        
        # Save results if requested
        if output:
            output_data = {
                'filename': result.filename,
                'processed_at': datetime.now().isoformat(),
                'total_sentences': len(result.sentences),
                'astrological_sentences': len(result.astrological_sentences),
                'sample_sentences': result.astrological_sentences[:10]
            }
            
            if extract_rules:
                output_data['extracted_rules'] = len(rules)
                output_data['stored_rules'] = stored_count if 'stored_count' in locals() else 0
            
            with open(output, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            click.echo(f"💾 Results saved to: {output}")
        
        click.echo(f"\n✅ Processing complete!")
        
    except Exception as e:
        click.echo(f"❌ Error processing book: {e}")


@cli.command()
@click.argument('directory', type=click.Path(exists=True), required=False)
@click.option('--authority', '-l',
              type=click.Choice(['classical', 'traditional', 'modern', 'commentary']),
              default='modern', help='Default authority level for all books')
@click.option('--extract-rules', '-r', is_flag=True, help='Extract and store rules')
def batch_process(directory, authority, extract_rules):
    """Process all PDFs in a directory (uses books directory from config if not specified)"""
    
    # Use configured books directory if none specified
    if directory is None:
        directory = str(get_books_dir())
        click.echo(f"📁 Using configured books directory: {directory}")
    
    pdf_files = list(Path(directory).glob("*.pdf"))
    
    if not pdf_files:
        click.echo(f"❌ No PDF files found in {directory}")
        return
    
    click.echo(f"📚 Found {len(pdf_files)} PDF files")
    
    processor = DocumentProcessor()
    extractor = RuleExtractor() if extract_rules else None
    kb = KnowledgeBase() if extract_rules else None  # Uses configuration for database path
    
    total_rules = 0
    
    authority_map = {
        'classical': AuthorityLevel.CLASSICAL,
        'traditional': AuthorityLevel.TRADITIONAL,
        'modern': AuthorityLevel.MODERN,
        'commentary': AuthorityLevel.COMMENTARY
    }
    
    for pdf_file in pdf_files:
        click.echo(f"\n🔄 Processing: {pdf_file.name}")
        
        try:
            # Process document
            result = processor.process_document(str(pdf_file))
            click.echo(f"   📊 {len(result.astrological_sentences)} astrological sentences found")
            
            # Extract rules if requested
            if extract_rules and result.astrological_sentences:
                source_info = SourceInfo(
                    title=pdf_file.stem,
                    authority_level=authority_map[authority]
                )
                
                rules = extractor.extract_rules_from_sentences(
                    result.astrological_sentences,
                    source_info
                )
                
                if rules:
                    stored_count = kb.store_rules_batch(rules)
                    total_rules += stored_count
                    click.echo(f"   ✅ Extracted and stored {stored_count} rules")
            
        except Exception as e:
            click.echo(f"   ❌ Error: {e}")
    
    click.echo(f"\n📊 Batch processing complete!")
    if extract_rules:
        click.echo(f"🎯 Total rules extracted and stored: {total_rules}")


@cli.command()
@click.option('--planet', '-p', help='Filter by planet')
@click.option('--house', '-h', type=int, help='Filter by house (1-12)')
@click.option('--sign', '-s', help='Filter by zodiac sign')
@click.option('--source', help='Filter by source title')
@click.option('--min-confidence', '-c', type=float, default=0.0, help='Minimum confidence score')
@click.option('--limit', '-l', type=int, help='Limit number of results')
@click.option('--export', '-e', type=click.Path(), help='Export results to JSON file')
def search_rules(planet, house, sign, source, min_confidence, limit, export):
    """Search for rules in the knowledge base"""
    
    kb = KnowledgeBase()  # Uses configuration for database path
    
    try:
        rules = kb.search_rules(
            planet=planet,
            house=house, 
            sign=sign,
            source=source,
            min_confidence=min_confidence,
            limit=limit
        )
        
        click.echo(f"🔍 Found {len(rules)} matching rules")
        
        if rules:
            click.echo(f"\n📝 Rules:")
            for i, rule in enumerate(rules, 1):
                click.echo(f"\n{i}. {rule.original_text}")
                click.echo(f"   Planet: {rule.conditions.planet}, House: {rule.conditions.house}, Sign: {rule.conditions.sign}")
                click.echo(f"   Effects: {', '.join([e.description[:50] for e in rule.effects])}")
                click.echo(f"   Source: {rule.source.title}")
                click.echo(f"   Confidence: {rule.confidence_score:.2f}")
        
        if export:
            export_data = {
                'search_criteria': {
                    'planet': planet,
                    'house': house,
                    'sign': sign,
                    'source': source,
                    'min_confidence': min_confidence
                },
                'results_count': len(rules),
                'rules': [
                    {
                        'id': rule.id,
                        'text': rule.original_text,
                        'planet': rule.conditions.planet,
                        'house': rule.conditions.house,
                        'sign': rule.conditions.sign,
                        'effects': [e.description for e in rule.effects],
                        'source': rule.source.title,
                        'confidence': rule.confidence_score
                    }
                    for rule in rules
                ]
            }
            
            with open(export, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            click.echo(f"💾 Search results exported to {export}")
        
    except Exception as e:
        click.echo(f"❌ Error searching rules: {e}")


@cli.command()
@click.option('--output', '-o', help='Output file path (uses configured export directory if not specified)')
def export_knowledge(output):
    """Export all rules from the knowledge base to JSON"""
    
    try:
        kb = KnowledgeBase()  # Uses configuration for database path
        
        # Use configured export path if not specified
        if output is None:
            output = str(get_export_path('knowledge_export.json'))
        
        exported_path = kb.export_rules_json(output)
        
        stats = kb.get_database_stats()
        click.echo(f"✅ Exported {stats['total_rules']} rules to: {exported_path}")
        
    except Exception as e:
        click.echo(f"❌ Error exporting knowledge base: {e}")


@cli.command()
def stats():
    """Show knowledge base statistics"""
    
    try:
        kb = KnowledgeBase()  # Uses configuration for database path
        stats = kb.get_database_stats()
        
        click.echo("📊 Knowledge Base Statistics")
        click.echo("=" * 40)
        click.echo(f"Total rules: {stats['total_rules']}")
        click.echo(f"Average confidence: {stats['average_confidence']:.2f}")
        
        if 'by_authority' in stats:
            click.echo("\n📚 Rules by Authority Level:")
            for authority, count in stats['by_authority'].items():
                click.echo(f"   {authority}: {count}")
        
        if 'by_planet' in stats:
            click.echo("\n🪐 Rules by Planet:")
            for planet, count in stats['by_planet'].items():
                click.echo(f"   {planet}: {count}")
        
    except Exception as e:
        click.echo(f"❌ Error getting statistics: {e}")


@cli.command()
def test_setup():
    """Test if the setup is working correctly"""
    
    click.echo("🧪 Testing Astrology AI setup...")
    
    # Test configuration
    try:
        config = get_config()
        if config:
            click.echo("✅ Configuration system loaded")
            
            # Validate setup
            validation = config.validate_setup()
            click.echo("\n📊 Configuration validation:")
            for check, result in validation.items():
                status = "✅" if result else "❌"
                click.echo(f"   {status} {check}: {result}")
        else:
            click.echo("⚠️  Using fallback configuration")
    except Exception as e:
        click.echo(f"❌ Configuration error: {e}")
    
    # Test imports
    try:
        import PyPDF2
        import pdfplumber
        import spacy
        click.echo("✅ Required packages imported successfully")
    except ImportError as e:
        click.echo(f"❌ Missing package: {e}")
        return
    
    # Test directories using configuration
    try:
        config = get_config()
        if config:
            required_dirs = [
                ('Books', config.directories.books_dir),
                ('Rules', config.directories.rules_dir), 
                ('Charts', config.directories.charts_dir),
                ('Exports', config.directories.exports_dir)
            ]
        else:
            # Fallback directories
            required_dirs = [
                ('Books', Path('data/books')),
                ('Rules', Path('data/rules')),
                ('Charts', Path('data/charts'))
            ]
        
        for name, dir_path in required_dirs:
            if dir_path.exists():
                click.echo(f"✅ {name} directory exists: {dir_path}")
            else:
                click.echo(f"❌ {name} directory missing: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
                click.echo(f"✅ Created {name} directory: {dir_path}")
    except Exception as e:
        click.echo(f"❌ Directory setup error: {e}")
    
    # Test components
    try:
        processor = DocumentProcessor()
        extractor = RuleExtractor()
        kb = KnowledgeBase()  # Uses configuration for database path
        click.echo("✅ All components initialized successfully")
    except Exception as e:
        click.echo(f"❌ Component initialization error: {e}")
        return
    
    # Test rule extraction
    test_sentence = "Mars in the 7th house causes conflicts in marriage"
    if processor.contains_astrological_content(test_sentence):
        click.echo("✅ Astrological content detection working")
    else:
        click.echo("❌ Astrological content detection failed")
    
    click.echo(f"\n🎉 Setup test complete! Ready to process astrology books.")
    click.echo(f"\n🚀 Next steps:")
    
    try:
        books_dir = get_books_dir()
        click.echo(f"   1. Add PDF books to {books_dir}")
        click.echo(f"   2. Run: python cli.py process-book {books_dir}/your_book.pdf --extract-rules")
    except:
        click.echo(f"   1. Add PDF books to data/books/")
        click.echo(f"   2. Run: python cli.py process-book data/books/your_book.pdf --extract-rules")
    
    click.echo(f"   3. View results: python cli.py stats")


@cli.command()
def config_info():
    """Show current configuration information"""
    
    try:
        config = get_config()
        if not config:
            click.echo("⚠️  Configuration system not available, using fallbacks")
            return
        
        click.echo("🔧 Current Configuration")
        click.echo("=" * 50)
        
        click.echo(f"Project Root: {config.directories.project_root}")
        click.echo(f"Data Directory: {config.directories.data_dir}")
        
        click.echo(f"\n📁 Directory Structure:")
        click.echo(f"   Books: {config.directories.books_dir}")
        click.echo(f"   Rules: {config.directories.rules_dir}")
        click.echo(f"   Charts: {config.directories.charts_dir}")
        click.echo(f"   Exports: {config.directories.exports_dir}")
        click.echo(f"   Logs: {config.directories.logs_dir}")
        click.echo(f"   Cache: {config.directories.cache_dir}")
        
        click.echo(f"\n🗄️  Database Paths:")
        click.echo(f"   Main: {config.get_database_path('main')}")
        click.echo(f"   Test: {config.get_database_path('test')}")
        
        click.echo(f"\n⚙️  Processing Settings:")
        click.echo(f"   Min sentence length: {config.processing.min_sentence_length}")
        click.echo(f"   Max sentence length: {config.processing.max_sentence_length}")
        click.echo(f"   Min confidence threshold: {config.processing.min_confidence_threshold}")
        click.echo(f"   OCR correction: {config.processing.enable_ocr_correction}")
        
    except Exception as e:
        click.echo(f"❌ Error getting configuration info: {e}")


if __name__ == '__main__':
    cli()