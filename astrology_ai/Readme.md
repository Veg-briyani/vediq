# 🌌 Astrology AI - Phase 1: Foundation & Rule Extraction

An AI system that learns from classical astrology texts and builds an intelligent knowledge base of astrological rules.

## 🎯 What This Does

- **Extracts text** from astrology PDF books
- **Identifies astrological content** using NLP patterns
- **Converts natural language** into structured rules
- **Stores knowledge** in a searchable database
- **Provides CLI tools** for exploration and analysis

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd astrology_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download language model
python -m spacy download en_core_web_sm
```

### 2. Initial Setup

```bash
# Set up directories and test the system
python main.py setup
python main.py test
```

### 3. Process Your First Book

```bash
# Add a PDF book to data/books/
# Then process it:
python main.py cli process-book data/books/your_book.pdf \
  --source-title "Your Book Title" \
  --author "Author Name" \
  --authority classical \
  --extract-rules \
  --show-samples
```

### 4. Explore the Knowledge Base

```bash
# Search for specific rules
python main.py cli search-rules --planet Mars
python main.py cli search-rules --house 7
python main.py cli search-rules --sign Leo

# View statistics
python main.py cli stats

# Run a demo with sample data
python main.py demo
```

## 📁 Project Structure

```
astrology_ai/
├── src/                     # Core system modules
│   ├── __init__.py         # Main system class
│   ├── data_models.py      # Data structures
│   ├── document_processor.py  # PDF text extraction
│   ├── rule_extractor.py   # NLP rule extraction
│   ├── knowledge_base.py   # Database storage
│   └── cli.py              # Command line interface
├── data/
│   ├── books/              # PDF storage
│   ├── rules/              # Extracted rules
│   └── charts/             # Generated charts
├── config/
│   └── sources.yaml        # Source authority hierarchy
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🔧 Core Components

### DocumentProcessor
Extracts and cleans text from astrology PDFs, identifying sentences that contain astrological content.

### RuleExtractor  
Uses NLP patterns to convert natural language into structured astrological rules with conditions and effects.

### KnowledgeBase
SQLite database system for storing, searching, and managing extracted rules with source attribution.

### CLI Interface
Command-line tools for processing books, searching rules, and managing the knowledge base.

## 📚 Usage Examples

### Process Multiple Books
```bash
# Process all PDFs in a directory
python main.py cli batch-process data/books/ --authority classical --extract-rules
```

### Advanced Searching
```bash
# Find high-confidence Mars rules
python main.py cli search-rules --planet Mars --min-confidence 0.7

# Export search results
python main.py cli search-rules --house 10 --export career_rules.json
```

### Export Knowledge Base
```bash
# Export all rules to JSON
python main.py cli export-knowledge --output my_astrology_knowledge.json
```

## 🎯 Phase 1 Goals

- [x] PDF text extraction and processing
- [x] Astrological content identification  
- [x] Natural language rule extraction
- [x] Structured knowledge storage
- [x] Command-line interface
- [x] Source authority management
- [x] Search and export capabilities

## 📊 Example Output

When you process a book, you'll see:
```
📚 Processing: Classical_Astrology_Book.pdf

📊 Processing Results:
   Document: Classical_Astrology_Book.pdf
   Total sentences: 2,847
   Astrological sentences: 423
   Content ratio: 14.9%

🔄 Extracting rules...
   Extracted 156 rules
   ✅ Stored 156 rules in knowledge base

📝 Sample extracted rules:
   1. Mars in the 7th house causes conflicts in marriage...
      Planet: Mars, House: 7
      Effects: 1, Confidence: 0.85
```

## 🔍 Search Results

```bash
$ python main.py cli search-rules --planet Jupiter

🔍 Found 23 matching rules

📝 Rules:

1. Jupiter in its own sign gives wisdom and prosperity
   Planet: Jupiter, House: None, Sign: None
   Effects: wisdom and prosperity
   Source: Brihat Parashara Hora Shastra
   Confidence: 0.92
```

## 🛠️ Development

### Adding New Features
The system is designed to be modular. Key extension points:

- **Add new extraction patterns** in `rule_extractor.py`
- **Enhance data models** in `data_models.py`  
- **Add new CLI commands** in `cli.py`
- **Modify authority hierarchy** in `config/sources.yaml`

### Testing
```bash
# Test individual components
python src/document_processor.py
python src/rule_extractor.py
python src/knowledge_base.py

# Full system test
python main.py test
```

## 📈 Next Steps (Phase 2)

- Chart calculation and interpretation
- Rule matching engine for birth charts
- Web interface for broader access
- Enhanced NLP with machine learning
- Multiple chart types (D-9, D-10, etc.)

## 🤝 Contributing

This is a personal learning project, but the architecture is designed to be:
- **Modular**: Easy to extend and modify
- **Well-documented**: Clear code with comprehensive comments
- **Testable**: Each component can be tested independently

## 📝 Notes

- Start with **classical texts** for highest quality rules
- The system learns and improves as you add more books
- **Authority levels** help resolve conflicting interpretations
- All extracted rules include **source attribution**

---

**Happy building!** 🌟 

You're creating a bridge between ancient wisdom and modern AI. Each book you process makes the system smarter and more knowledgeable about the timeless art of astrology.