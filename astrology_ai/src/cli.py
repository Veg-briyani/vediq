# src/cli.py
"""
Complete Command Line Interface for Astrology AI Phase 1
Integrates document processing, rule extraction, and knowledge storage
"""

import click
from pathlib import Path
import json
import yaml
from datetime import datetime

# Import our modules
from document_processor import DocumentProcessor
from rule_extractor import RuleExtractor
from knowledge_base import KnowledgeBase
from data_models import SourceInfo, AuthorityLevel


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
            
            # Store in knowledge base
            if rules:
                kb = KnowledgeBase()
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
@click.argument('directory', type=click.Path(exists=True))
@click.option('--authority', '-l',
              type=click.Choice(['classical', 'traditional', 'modern', 'commentary']),
              default='modern', help='Default authority level for all books')
@click.option('--extract-rules', '-r', is_flag=True, help='Extract and store rules')
def batch_process(directory, authority, extract_rules):
    """Process all PDFs in a directory"""
    
    pdf_files = list(Path(directory).glob("*.pdf"))
    
    if not pdf_files:
        click.echo(f"❌ No PDF files found in {directory}")
        return
    
    click.echo(f"📚 Found {len(pdf_files)} PDF files")
    
    processor = DocumentProcessor()
    extractor = RuleExtractor() if extract_rules else None
    kb = KnowledgeBase() if extract_rules else None
    
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
    
    kb = KnowledgeBase()
    
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
def stats():
    """Show knowledge base statistics"""
    
    try:
        kb = KnowledgeBase()
        stats = kb.get_database_stats()
        
        click.echo("📊 Knowledge Base Statistics")
        click.echo("=" * 40)
        click.echo(f"Total rules: {stats['total_rules']}")
        click.echo(f"Unique sources: {stats['unique_sources']}")
        click.echo(f"Average confidence: {stats['average_confidence']}")
        
        if stats['planet_distribution']:
            click.echo(f"\n🪐 Planet distribution:")
            for planet, count in stats['planet_distribution'].items():
                click.echo(f"   {planet}: {count}")
        
        if stats['house_distribution']:
            click.echo(f"\n🏠 House distribution:")
            for house, count in stats['house_distribution'].items():
                click.echo(f"   House {house}: {count}")
        
    except Exception as e:
        click.echo(f"❌ Error getting stats: {e}")


@cli.command()
@click.option('--output', '-o', default='data/knowledge_export.json', 
              help='Output file path')
def export_knowledge(output):
    """Export all rules to JSON file"""
    
    try:
        kb = KnowledgeBase()
        kb.export_rules_json(output)
        click.echo(f"✅ Knowledge base exported to {output}")
        
    except Exception as e:
        click.echo(f"❌ Error exporting: {e}")


@cli.command()
def test_setup():
    """Test if the setup is working correctly"""
    
    click.echo("🧪 Testing Astrology AI setup...")
    
    # Test imports
    try:
        import PyPDF2
        import pdfplumber
        import spacy
        click.echo("✅ Required packages imported successfully")
    except ImportError as e:
        click.echo(f"❌ Missing package: {e}")
        return
    
    # Test directories
    required_dirs = ['data/books', 'data/rules', 'data/charts']
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            click.echo(f"✅ Directory exists: {dir_path}")
        else:
            click.echo(f"❌ Directory missing: {dir_path}")
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            click.echo(f"✅ Created directory: {dir_path}")
    
    # Test components
    try:
        processor = DocumentProcessor()
        extractor = RuleExtractor()
        kb = KnowledgeBase()
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
    click.echo(f"   1. Add PDF books to data/books/")
    click.echo(f"   2. Run: python cli.py process-book data/books/your_book.pdf --extract-rules")
    click.echo(f"   3. View results: python cli.py stats")


@cli.command()
def demo():
    """Run a demonstration with sample data"""
    
    click.echo("🎯 Running Astrology AI demonstration...")
    
    # Create demo rules
    from data_models import create_simple_rule
    
    demo_rules = [
        create_simple_rule(
            "Mars in the 7th house causes conflicts in marriage",
            "Demo Astrology Book",
            planet="Mars",
            house=7,
            effect_desc="conflicts in marriage"
        ),
        create_simple_rule(
            "Jupiter in its own sign gives wisdom and prosperity", 
            "Demo Astrology Book",
            planet="Jupiter",
            effect_desc="wisdom and prosperity"
        ),
        create_simple_rule(
            "Sun in the 10th house brings success in career",
            "Demo Astrology Book", 
            planet="Sun",
            house=10,
            effect_desc="success in career"
        )
    ]
    
    # Store demo rules
    kb = KnowledgeBase()
    stored_count = kb.store_rules_batch(demo_rules)
    
    click.echo(f"✅ Created {stored_count} demo rules")
    
    # Show some searches
    click.echo(f"\n🔍 Demo searches:")
    
    mars_rules = kb.search_rules(planet="Mars")
    click.echo(f"   Mars rules: {len(mars_rules)}")
    
    house7_rules = kb.search_rules(house=7)
    click.echo(f"   7th house rules: {len(house7_rules)}")
    
    # Show stats
    stats = kb.get_database_stats()
    click.echo(f"\n📊 Demo database stats:")
    click.echo(f"   Total rules: {stats['total_rules']}")
    
    click.echo(f"\n✅ Demo complete! Try 'python cli.py search-rules --planet Mars'")


if __name__ == '__main__':
    cli()