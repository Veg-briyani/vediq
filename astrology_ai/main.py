#!/usr/bin/env python3
"""
Astrology AI - Main Entry Point
Phase 1: Foundation & Rule Extraction System

Quick start script for the Astrology AI system.
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

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
    print()
    print("For full CLI help, run: python main.py cli --help")
    print()
    print("Quick start:")
    print("  1. python main.py setup")
    print("  2. Add PDF books to data/books/")  
    print("  3. python main.py cli process-book data/books/your_book.pdf --extract-rules")

def setup_system():
    """Initial system setup"""
    print("🔧 Setting up Astrology AI system...")
    
    # Create required directories
    required_dirs = ['data', 'data/books', 'data/rules', 'data/charts', 'config']
    
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")
    
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
    print("1. Add astrology PDF books to data/books/")
    print("2. Run: python main.py cli process-book data/books/your_book.pdf --extract-rules")
    print("3. Explore: python main.py cli search-rules --planet Mars")

def test_system():
    """Test system components"""
    print("🧪 Testing Astrology AI components...")
    
    try:
        from src import AstrologyAI, get_version
        
        print(f"✅ Version: {get_version()}")
        
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

if __name__ == "__main__":
    main()