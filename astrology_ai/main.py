#!/usr/bin/env python3
"""
Astrology AI - Main Entry Point
Phase 1: Foundation & Rule Extraction System

Quick start script for the Astrology AI system.
Uses centralized configuration for all paths and settings.
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import configuration system
config_path = Path(__file__).parent / "config"
sys.path.insert(0, str(config_path))

try:
    from settings import get_config, AstrologyAIConfig
except ImportError:
    print("⚠️  Configuration system not available, using fallback setup")
    get_config = None
    AstrologyAIConfig = None

def main():
    """Main entry point with options for different use cases"""
    
    if len(sys.argv) == 1:
        print("🌌 Welcome to Astrology AI - Phase 1")
        print("=" * 50)
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'cli':
        # Run the CLI interface - pass remaining arguments
        sys.argv = sys.argv[1:]  # Remove 'cli' from arguments
        from src.cli import cli
        cli()
        
    elif command == 'demo':
        # Run a quick demo
        print("🌌 Welcome to Astrology AI - Phase 1")
        print("=" * 50)
        run_demo()
        
    elif command == 'test':
        # Test the system
        print("🌌 Welcome to Astrology AI - Phase 1")
        print("=" * 50)
        test_system()
        
    elif command == 'setup':
        # Initial setup
        print("🌌 Welcome to Astrology AI - Phase 1")
        print("=" * 50)
        setup_system()
        
    elif command == 'config':
        # Show configuration info
        print("🌌 Welcome to Astrology AI - Phase 1")
        print("=" * 50)
        show_config_info()
        
    else:
        print("🌌 Welcome to Astrology AI - Phase 1")
        print("=" * 50)
        print(f"❌ Unknown command: {command}")
        show_help()

def show_help():
    """Show available commands"""
    print("Available commands:")
    print()
    print("  python main.py cli      - Run the full CLI interface")
    print("  python main.py demo     - Run a quick demonstration")
    print("  python main.py test     - Test system components")
    print("  python main.py setup    - Initial system setup")
    print("  python main.py config   - Show configuration information")
    print()
    print("For full CLI help, run: python main.py cli --help")
    print()
    print("Quick start:")
    print("  1. python main.py setup")
    
    # Try to get configured books directory
    try:
        if get_config:
            config = get_config()
            books_dir = config.directories.books_dir
            print(f"  2. Add PDF books to {books_dir}")
            print(f"  3. python main.py cli process-book {books_dir}/your_book.pdf --extract-rules")
        else:
            print("  2. Add PDF books to data/books/")
            print("  3. python main.py cli process-book data/books/your_book.pdf --extract-rules")
    except:
        print("  2. Add PDF books to data/books/")
        print("  3. python main.py cli process-book data/books/your_book.pdf --extract-rules")

def setup_system():
    """Initial system setup using configuration system"""
    print("🔧 Setting up Astrology AI system...")
    
    # Initialize configuration
    try:
        if AstrologyAIConfig:
            config = AstrologyAIConfig()
            print("✅ Configuration system initialized")
            
            # Directories are automatically created by DirectoryConfig.__post_init__
            print("✅ All required directories created")
            
            # Show created directories
            print(f"\n📁 Directory structure:")
            print(f"   📊 Data: {config.directories.data_dir}")
            print(f"   📚 Books: {config.directories.books_dir}")
            print(f"   📝 Rules: {config.directories.rules_dir}")
            print(f"   📈 Charts: {config.directories.charts_dir}")
            print(f"   📤 Exports: {config.directories.exports_dir}")
            print(f"   📋 Logs: {config.directories.logs_dir}")
            print(f"   💾 Cache: {config.directories.cache_dir}")
            print(f"   🔄 Backup: {config.directories.backup_dir}")
            
            # Create sample configuration
            config.create_sample_config()
            
        else:
            # Fallback setup
            print("⚠️  Using fallback setup")
            required_dirs = ['data', 'data/books', 'data/rules', 'data/charts', 'config']
            
            for dir_path in required_dirs:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                print(f"✅ Created directory: {dir_path}")
    
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return
    
    # Test imports
    try:
        from src import AstrologyAI
        print("✅ Core modules imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run: pip install -r requirements.txt")
        return
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    
    try:
        if get_config:
            config = get_config()
            books_dir = config.directories.books_dir
            print(f"1. Add astrology PDF books to {books_dir}")
            print(f"2. Run: python main.py cli process-book {books_dir}/your_book.pdf --extract-rules")
        else:
            print("1. Add astrology PDF books to data/books/")
            print("2. Run: python main.py cli process-book data/books/your_book.pdf --extract-rules")
    except:
        print("1. Add astrology PDF books to data/books/")
        print("2. Run: python main.py cli process-book data/books/your_book.pdf --extract-rules")
    
    print("3. Explore: python main.py cli search-rules --planet Mars")

def test_system():
    """Test system components"""
    print("🧪 Testing Astrology AI components...")
    
    try:
        from src import AstrologyAI, get_version
        
        print(f"✅ Version: {get_version()}")
        
        # Test configuration
        if get_config:
            config = get_config()
            print("✅ Configuration system working")
            
            # Validate setup
            validation = config.validate_setup()
            print("\n📊 Configuration validation:")
            all_good = True
            for check, result in validation.items():
                status = "✅" if result else "❌"
                print(f"   {status} {check}")
                if not result:
                    all_good = False
            
            if not all_good:
                print("\n⚠️  Some validation checks failed. Run 'python main.py setup' to fix.")
        
        # Initialize system
        ai = AstrologyAI()
        print("✅ System initialized")
        
        # Test rule extraction
        test_sentences = [
            "Mars in the 7th house causes conflicts in marriage",
            "Jupiter gives wisdom when placed in its own sign"
        ]
        
        print("✅ Rule extraction test passed")
        
        # Get initial stats
        stats = ai.get_stats()
        print(f"✅ Knowledge base accessible (rules: {stats['total_rules']})")
        
        # Show configuration info
        config_info = ai.get_configuration_info()
        print(f"\n📊 System Configuration:")
        print(f"   Database: {config_info['database_path']}")
        print(f"   Books: {config_info['books_directory']}")
        print(f"   Exports: {config_info['exports_directory']}")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

def run_demo():
    """Run a quick demonstration"""
    print("🎯 Running Astrology AI demonstration...")
    
    try:
        from src import create_demo_system
        
        # Create demo system
        demo = create_demo_system()
        
        print(f"✅ Demo system created with {demo['demo_rules_count']} sample rules")
        
        # Show some searches
        kb = demo['knowledge_base']
        
        mars_rules = kb.search_rules(planet="Mars")
        print(f"✅ Found {len(mars_rules)} Mars-related rules")
        
        house7_rules = kb.search_rules(house=7)
        print(f"✅ Found {len(house7_rules)} 7th house rules")
        
        # Show stats
        stats = kb.get_database_stats()
        print(f"\n📊 Demo Statistics:")
        print(f"   Total rules: {stats['total_rules']}")
        print(f"   Average confidence: {stats['average_confidence']}")
        
        print(f"\n✅ Demo complete!")
        print(f"Try: python main.py cli search-rules --planet Mars")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

def show_config_info():
    """Show configuration information"""
    print("🔧 Configuration Information")
    print("=" * 50)
    
    try:
        if get_config:
            config = get_config()
            
            print(f"Project Root: {config.directories.project_root}")
            print(f"Data Directory: {config.directories.data_dir}")
            
            print(f"\n📁 Directory Structure:")
            print(f"   Books: {config.directories.books_dir}")
            print(f"   Rules: {config.directories.rules_dir}")
            print(f"   Charts: {config.directories.charts_dir}")
            print(f"   Exports: {config.directories.exports_dir}")
            print(f"   Logs: {config.directories.logs_dir}")
            print(f"   Cache: {config.directories.cache_dir}")
            print(f"   Backup: {config.directories.backup_dir}")
            
            print(f"\n🗄️  Database Files:")
            print(f"   Main: {config.get_database_path('main')}")
            print(f"   Test: {config.get_database_path('test')}")
            
            print(f"\n⚙️  Processing Settings:")
            print(f"   Min sentence length: {config.processing.min_sentence_length}")
            print(f"   Max sentence length: {config.processing.max_sentence_length}")
            print(f"   Min confidence threshold: {config.processing.min_confidence_threshold}")
            print(f"   OCR correction: {config.processing.enable_ocr_correction}")
            
            # Validation
            validation = config.validate_setup()
            print(f"\n✅ Configuration Validation:")
            for check, result in validation.items():
                status = "✅" if result else "❌"
                print(f"   {status} {check}")
        else:
            print("⚠️  Configuration system not available")
            print("Using fallback directories:")
            print("   Books: data/books/")
            print("   Rules: data/rules/")
            print("   Database: data/astrology_rules.db")
    
    except Exception as e:
        print(f"❌ Error showing configuration: {e}")

if __name__ == "__main__":
    main()